# Lambda function to extract data from a source
# Trigger: S3 object that ends with .config

import os
import json
import logging

import boto3
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.resource('s3')

def lambda_handler(event, context):
    assert len(event['Records']) == 1, \
        build_response(500, 'Multiple records provided by input S3 event')

    storage = event['Records'][0].get('s3')

    bucket = storage['bucket']['name']
    object = storage['object']['key'] # file that triggered function (ending with .config)

    try:
        log('fetching the job config from s3')
        config = get_object(bucket, object)

        output, next = build_paths(object)
        log(f'function will produce {output} on complete')

        log(f'starting extract for {config["extract"]}')
        globals()[config['extract']](config, bucket, output, next)

        build_response(200, 'data extracted successfully from source')
    except Exception as e:
        return build_response(500, e)

# Extract functions

def arcgis(job, bucket, output, next):
    fetch = job['request']

    if not 'resultOffset' in fetch['params']:
        fetch['params']['resultOffset'] = 0

    log(f'extracting data from arcgis source with offset {fetch["params"]["resultOffset"]}')

    r = requests.get(**fetch)
    data = json.loads(r.content)

    if data.get('properties', {}).get('exceededTransferLimit', False):
        fetch['params']['resultOffset'] += len(data['features'])
        log(f'initializing next extract pagination with offset {fetch["params"]["resultOffset"]} and config file {next}')

        s3.Bucket(bucket).put_object(Body=json.dumps(job).encode(), Key=next)

    log('saving extracted data to s3')
    s3.Bucket(bucket).put_object(Body=r.content, Key=output)

# Utilities functions

def build_paths(path):
    dir, f = os.path.split(path)
    fn, ext = os.path.splitext(f)

    return os.path.join(dir, f'{fn}.extract'), os.path.join(dir, f'{1 + int(fn)}.config')

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

def get_object(bucket, object):
    f = s3.Bucket(bucket).Object(object).get()

    return json.loads(f['Body'].read())

def log(msg):
    logging.info(msg)
