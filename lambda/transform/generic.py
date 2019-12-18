import geopandas as gpd
import numpy as np
import pandas as pd

import builtins

from datetime import datetime


def get_type(series):
    if series.name == 'geometry' and isinstance(series, gpd.GeoSeries):
        return 'geometry'

    try:
        distinct_count = series.nunique()
        value_count = series.nunique(dropna=False)

        if value_count == 1 and distinct_count == 0:
            return 'empty'
        elif pd_types.is_bool_dtype(series):
            return 'bool'
        elif pd_types.is_datetime64_dtype(series):
            # TODO: date and datetime?
            return 'date'
        elif pd_types.is_numeric_dtype(series):
            return 'numeric'
        else:
            return 'text'
    except:
        # eg. 2D series
        return 'unknown'

def transform(config, details):
    if 'transform' in details:
        data = pd.read_feather(details['transform']['file'])
        details['transform']['file'] = f'../s3/etl/{config["jobID"]}_processed_{details["start"]}.csv'
    else:
        details['transform'] = {
            'init': int(round(time.time())),
            'logs': [],
            'file': f'../s3/etl/{config["jobID"]}_processed_{details["start"]}.csv',
            'success': False
        }

        _, fmt = details['extract']['file'].split('.')

        if fmt == 'json':
            data = pd.read_json(config['raw'])
        elif fmt == 'csv':
            data = pd.read_csv(config['raw'])
        else:
            # Raise error for unable to load data or something
            pass

    data = data[[field['id'] for field in config['fields']]]

    for field in config['fields']:
        if field['type'] in ['bool', 'int', 'float']:
            data[field['id']] = data[field['id']].apply(
                lambda x: getattr(builtins, field['type'])(x)
                    if not pd.isnull(x) else None
            )
        elif field['type'] in ['timestamp']:
            # TODO: Not sure if this should be "generic"
            data[column] = data[column].apply(
                lambda x: datetime.utcfromtimestamp(x / 1000).strftime('%Y-%m-%d %H:%M:%S') if not pd.isnull(x) else None
            )

    data.to_csv(details['transform']['file'], index=False)

    details['transform']['success'] = True
