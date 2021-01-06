import json
import boto3
import datetime

region = 'eu-west-1'
instance_ids = ['i-0ec68716f022813ca']
ec2 = boto3.resource('ec2', region_name=region)
client = boto3.client('ses', region_name=region)

def lambda_handler(event, context):
    for i in instance_ids:
        instance = ec2.Instance(i)
        print(instance.state['Name'])
        print(instance.launch_time)

        now = datetime.datetime.now()
        now = now.replace(tzinfo=None)
        launch = instance.launch_time.replace(tzinfo=None)

        if (now - launch).total_seconds() > 10 and instance.state['Name']== 'running':
            print("Sending mail")
            response = client.send_email(
                Source='support@dev.aws-standardbank.com',
                Destination={
                    'ToAddresses': [
                        'GauravKumar.Gupta@softwareag.com',
                    ],
                    'CcAddresses': [
                        'GauravKumar.Gupta@softwareag.com',
                    ]
                },
                Message={
                    'Subject': {
                        'Data': 'EC2 Instance running long',
                        'Charset': 'UTF-8'
                    },
                    'Body': {
                        'Text': {
                            'Data': 'This EC2 instance has been running for more than 24 hours',
                            'Charset': 'UTF-8'
                        },
                        'Html': {
                            'Data': 'This EC2 instance has been running for more than 24 hours',
                            'Charset': 'UTF-8'
                        }
                    }
                }
            )