import base64
import importlib
import json
import os

import requests

import extract
import load

from urllib.parse import unquote, urljoin

from flask import Flask, request


app = Flask(__name__)


@app.route('/extract/<job_id>', methods=['GET'])
def dump(job_id):
    path = os.path.join('../dynamodb', f'{job_id}.json')

    with open(path, 'rb') as f:
        config = json.load(f)

    config['raw'] = getattr(extract, config['extractType'])(config)

    with open(path, 'w') as f:
        json.dump(config, f)

    return build_response(200)

@app.route('/transform/<job_id>', methods=['GET'])
def transform(job_id):
    path = os.path.join('../dynamodb', f'{job_id}.json')

    with open(path, 'rb') as f:
        config = json.load(f)

    func = importlib.import_module(f'transform.{config["transformType"]}')
    config['processed'] = func.transform(config)

    with open(path, 'w') as f:
        json.dump(config, f)

    return build_response(200)

# def lambda_handler(event, context):
#     try:
#         if event['isBase64Encoded']:
#             params = json.loads(
#                 base64.decodebytes(event['body'].encode('utf-8'))
#             )
#         else:
#             params = json.loads(unquote(event['body']))
#
#         if not 'url' in params
#             return build_response(400, 'Missing required CKAN or package information')
#
#         if not ('step' in params and params['step'] in ['display', 'replicate']):
#             return build_response(400, 'Invalid step parameter provided')
#
#     except ValueError as e:
#         return build_response(400, 'Provided input parameters can not be parsed')

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

if __name__ == "__main__":
    app.run(debug=True)
