# Lambda function to build scheduler as a AWS CloudWatch Event rule
# Trigger: API Gateway POST request with job config

import json

import boto3

cw = boto3.client('events')
s3 = boto3.resource('s3')

BUCKET_CONFIG = 'aws-od-configs'

LAMBDA_ROLE = ''
LAMBDA_TRIGGER = ''

def lambda_handler(event, context):
    try:
        config = json.loads(event['body'])
        job_id = config.get('id')

        s3.Bucket(
            BUCKET_CONFIG
        ).put_object(
            Body=event['body'].encode(),
            Key=f'${job_id}.json'
        )

        rule = cw.put_rule(
            Name=job_id,
            ScheduleExpression=f'cron({config.get("cron")})',
            State='ENABLED',
            RoleArn=LAMBDA_ROLE
        )

        target = cw.put_targets(
            Rule=job_id,
            Targets=[{
                'Arn': LAMBDA_TRIGGER,
                'Id': 'InitPipelineJob', # ID of the target for this specific rule
                'Input': json.dumps({'id': job_id})
            }]
        )

        return build_response(200, f'successfully created scheduler with ARN {rule["RuleArn"]}')
    except Exception as e:
        return build_response(500, e)

def build_response(code, message=''):
    response = {
        'statusCode': code,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        }
    }

    if message:
        response['body'] = message

    return response
