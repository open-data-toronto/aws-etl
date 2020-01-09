# Lambda function to trigger a pipeline run by re-creating a new job config file
# Trigger: AWS CloudWatch Event on a cron schedule

import boto3

from datetime import datetime as dt

s3 = boto3.resource('s3')

BUCKET_CONFIG = 'aws-od-configs'
BUCKET_PIPELINE = 'aws-od-pipelines'

def lambda_handler(event, context):
    try:
        s3.meta.client.copy_object(
            CopySource={
                'Bucket': BUCKET_CONFIG,
                'Key': f'{event["job"]}.json'
            },
            Bucket=BUCKET_PIPELINE,
            Key=f'{event["job"]}/{dt.now().isoformat()}/0.config'
        )

        return build_response(200, f'successfully triggered pipeline for {event["job"]}')
    except Exception as e:
        return build_response(500, e)

def build_response(code, message=''):
    response = {
        'statusCode': code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        }
    }

    if message:
        response['body'] = message

    return response
