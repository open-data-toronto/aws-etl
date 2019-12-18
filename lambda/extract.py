import requests

import util


def api(config, details):
    details['extract'] = {
        'init': int(round(time.time())),
        'logs': [],
        'file': f'../s3/etl/{config["jobID"]}_raw_{details["start"]}.{config["dataType"]}',
        'success': False
    }

    logs = details['extract']['logs']

    # TODO: paginate data loading
    utils.log(logs, 'fetching data from source')
    r = requests.get(**config['request'])

    utils.log(logs, 'caching data to s3')
    with open(details['extract']['file'], 'wb') as f:
        f.write(r.content)

    details['extract']['success'] = True
