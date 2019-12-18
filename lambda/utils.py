import json
import os
import time

CONFIG_PATH = '../s3/jobs'
LOGS_PATH = '../s3/logs'

def init_job(job_id):
    # TODO: Validate config file exist at location
    config_loc = os.path.join(CONFIG_PATH, f'{job_id}.json')
    logs_loc = os.path.join(LOG_PATH, f'{job_id}_summary.txt')

    with open(config_loc, 'rb') as f:
        config = json.load(f)

    if not os.path.exists(logs_loc):
        logs = []
    else:
        with open(logs_loc, 'rb') as f:
            logs = sorted(json.load(f), key=lambda l: l['start'])

    if len(logs) >= 5:
        logs = logs[1:6]

    logs.insert(0, { 'start': int(round(time.time())) })

    return config, logs

def log(logs, message):
    logs.append((
        int(round(time.time())), message
    ))

def save_summary(job_id, logs):
    with open(os.path.join(LOG_PATH, f'{job_id}_summary.txt'), 'w') as f:
        json.dump(logs, f)
