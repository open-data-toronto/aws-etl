import geopandas as gpd
import numpy as np
import pandas as pd

import csv
import io
import json
import os

from transform import generic

from datetime import datetime

from shapely.geometry import mapping


def geometry_to_record(row):
    if not row is None:
        row = mapping(row)

        row['coordinates'] = np.asarray(row['coordinates']).tolist()

    return json.dumps(row)

def transform(config):
    config['processed'] = config['raw'].replace(
        config['dataType'], 'feather'
    ).replace(
        '_raw_', '_processed_'
    )

    data = gpd.read_file(config['raw']).to_crs(epsg=4326)
    data['geometry'] = data['geometry'].apply(lambda x: geometry_to_record(x))

    data.to_feather(config['processed'])

    return generic.transform(config)
