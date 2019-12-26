import os
import json

import boto3
import request

s3 = boto3.resource('s3')

def lambda_handler(event, context):
    assert len(event['Records']) == 0, \
        build_response(500, 'Multiple records provided by input S3 event')

    storage = event['Records'][0].get('s3')

    bucket = storage['bucket']['name']
    object = storage['object']['key']

    try:
        job = json.loads(get_object(bucket, object))
        output, next = build_paths(object, job['dataType'])

        globals()[job['extract']](job, bucket, output, next)
    except:
        return build_response(500, 'Something bad happened')

def arcgis(job, bucket, output, next):
    fetch = job['request']

    if not 'resultOffset' in fetch['params']:
        fetch['params']['resultOffset'] = 0

    r = requests.get(**fetch)
    data = json.loads(r.content)

    if data.get('properties', {}).get('exceededTransferLimit', False):
        fetch['params']['resultOffset'] += len(data['features'])

        s3.put_object(Body=json.dumps(job).encode(), Bucket=bucket, Key=next)

    s3.put_object(Body=r.content, Bucket=bucket, Key=output)

def build_paths(path, type):
    dir, f = os.path.split(path)
    fn, ext = os.path.splitext(f)

    # TODO: validate file name

    return os.path.join(dir, f'{fn}.{type}'),
        os.path.join(dir, f'{1 + int(fn)}.config')

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
    f = s3.Object(bucket, object).get()

    return f['Body'].read()
