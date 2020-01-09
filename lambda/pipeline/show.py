# Lambda function to build scheduler as a AWS CloudWatch Event rule
# Trigger: API Gateway with job (package_id) and cron with query parameters

import boto3

cw = boto3.client('events')

aws_role = ''
aws_lambda = ''

def lambda_handler(event, context):
    try:
        params = event['queryStringParameters']

        job = params.get('job')
        cron = params.get('cron')

        rule = cw.put_rule(
            Name=job,
            ScheduleExpression=f'cron({cron})',
            EventPattern='string',
            State='ENABLED',
            RoleArn=aws_role
        )

        target = cw.put_targets(
            Rule=job,
            Targets=[{
                'Arn': aws_lambda,
                'Id': 'InitPipelineJob', # ID of the target for this specific rule
            }]
        )

        return build_response(200, f'successfully created scheduler with ARN {rule["RuleArn"]}')
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
