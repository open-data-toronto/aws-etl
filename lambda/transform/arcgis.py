import geopandas as gpd
import shapely.geometry as geometry

import json

import utils

from transform import generic


def geometry_to_record(row):
    if not row is None:
        row = geometry.mapping(row)

    return json.dumps(row)

def transform(config, details):
    details['transform'] = {
        'init': int(round(time.time())),
        'logs': [],
        'file': f'../s3/etl/{config["jobID"]}_processed_{details["start"]}.feather',
        'success': False
    }

    logs = details['transform']['log']

    # TODO: filter out empty geometries
    utils.log(logs, 'reading file from cache')
    data = gpd.read_file(config['raw']).to_crs(epsg=4326)

    utils.log(logs, 'parsing geometry object to JSON string')
    data['geometry'] = data['geometry'].apply(lambda x: geometry_to_record(x))

    utils.log(logs, 'caching data to s3')
    data.to_feather(config['processed'])

    generic.transform(config, details)
