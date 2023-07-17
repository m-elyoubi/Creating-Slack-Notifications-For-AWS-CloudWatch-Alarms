# Creating Slack Notifications for CloudWatch Alarms
To post a Slack notification for CloudWatch Alarms when an EC2 instance's CPU utilization reaches greater than 40%, you can follow these steps:
## Set up an Incoming Webhook in Slack:

1. Create a Slack App: <https://api.slack.com/apps/new>
1. Search for and select **Incoming WebHooks**.
1. Set **Activate Incoming Webhooks** to **On**.
1. Select **Add New Webhook to Workspace**.
1. Choose the default channel where messages will be sent and click **Authorize**.
1. Note the webhook URL from the **Webhook URLs for Your Workspace** section. For example, `https://hooks.slack.com/services/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`

```sh
WEBHOOK_URL=https://hooks.slack.com/services/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
```

Test the webhook:

```sh
curl -X POST -H 'Content-type: application/json' --data '{"text":"Hello, World!"}' $WEBHOOK_URL
```

## Create an SNS Topic:

```sh
aws sns create-topic --name high-cpu-alarms
```

Note the `TopicArn`.

## Create CloudWatch Alarm:

Send notification to SNS topic when CPU utilization > 45%:

```sh
aws cloudwatch put-metric-alarm \
    --alarm-name cpu-mon \
    --alarm-description "Alarm when CPU exceeds 45%" \
    --metric-name CPUUtilization \
    --namespace AWS/EC2 \
    --statistic Average \
    --period 60 \
    --evaluation-periods 1 \
    --threshold 40 \
    --comparison-operator GreaterThanThreshold \
    --dimensions Name=InstanceId,Value=i-12345678901234567 \
    --alarm-actions arn:aws:sns:us-east-1:123456789012:high-cpu-alarms \
    --unit Percent
```

## Create SSM Parameter:

```sh
aws ssm put-parameter --cli-input-json '{"Type": "SecureString", "KeyId": "alias/aws/ssm", "Name": "/slack/webhook-url", "Value": "'"$WEBHOOK_URL"'"}'
```

## Create Lambda Execution Role:

Attach the following managed policies:

- AmazonSSMFullAccess
- AWSLambdaBasicExecutionRole

## Create Lambda Function:

Use the SNS topic as a trigger.

## Stress the CPU:

```sh
# Install Extra Packages for Enterprise Linux
sudo amazon-linux-extras install epel
# Install stress
sudo yum install -y stress
# Beat it up for 5 mins
stress --cpu 2 --timeout 300s
```

## After message Posted to Slack:
```sh
![slack](https://github.com/m-elyoubi/Creating-Slack-Notifications-for-CloudWatch-Alarms/assets/100800360/439cfb8d-caf5-49c6-a113-1a8089086c64)

``` 


