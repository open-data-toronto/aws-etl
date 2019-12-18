import base64
import importlib
import json
import os

import requests

import extract
import load
import utils

from urllib.parse import unquote, urljoin


def execute(job_id):
    config, summary = utils.init_job(job_id)

    tf = importlib.import_module(f'transform.{config["transformType"]}')

    logs = summary[0]
    try:
        getattr(extract, config['extractType'])(config, logs)
        tf.transform(config, logs)
    except:
        utils.save_logs(summary)

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
