# Lambda function to fetch the config of a specific job
# Trigger: API Gateway GET request with job ID

import boto3

cw = boto3.client('events')
s3 = boto3.resource('s3')

BUCKET_CONFIG = 'aws-od-configs'

def lambda_handler(event, context):
    try:
        params = event.get('queryStringParameters')
        if params.get('id', False):
            f = s3.Bucket(BUCKET_CONFIG).Object(f'{params.get("id")}.json').get()
            body = f['Body'].read().decode('utf-8')
        else:
            body = cw.list_rules()

        return build_response(200, body)
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
