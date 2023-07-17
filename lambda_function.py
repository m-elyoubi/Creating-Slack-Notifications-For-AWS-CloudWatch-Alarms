import json
import urllib.request

import boto3

def lambda_handler(event, context):
    try:
        # Retrieve the Slack webhook URL from Parameter Store
        ssm = boto3.client('ssm')
        parameter_name = '/slack/webhook-url'
        response = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
        webhook_url = response['Parameter']['Value']
        
        # Extract information from the SNS event payload
        sns_message = event['Records'][0]['Sns']['Message']
        alarm_message = json.loads(sns_message)['AlarmDescription']
        alarm_name = json.loads(sns_message)['AlarmName']
        new_state =json.loads(sns_message)['NewStateValue']
        reason = json.loads(sns_message)['NewStateReason']
        
        # Compose the message to send to Slack
        slack_message = {
            'text': f"CloudWatch Alarm triggered: {alarm_name} state is now {new_state}: {reason}'\n'"
                f'```\n{sns_message}```'
        }
        
        # Send the notification to Slack
        send_slack_notification(slack_message, webhook_url)
        
        return {
            'statusCode': 200,
            'body': 'Slack notification sent successfully'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Slack notification failed: {str(e)}'
        }

def send_slack_notification(message, webhook_url):
    try:
        req = urllib.request.Request(
            webhook_url,
            data=json.dumps(message).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        response = urllib.request.urlopen(req)
        # Uncomment the following line if you want to log the Slack API response
        print(response.read())
    except Exception as e:
        raise Exception(f'Failed to send Slack notification: {str(e)}')
