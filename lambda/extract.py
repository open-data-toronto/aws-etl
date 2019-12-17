import os
import time

import requests

def api(config):
    now = int(round(time.time()))
    path = f'../s3/{config["jobID"]}_raw_{now}.{config["dataType"]}'

    r = requests.get(**config['request'])
    with open(path, 'wb') as f:
        f.write(r.content)

    return path
