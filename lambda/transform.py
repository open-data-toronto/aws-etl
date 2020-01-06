import builtins
import io
import json
import os

import boto3
import geopandas as gpd
import numpy as np
import pandas as pd
import shapely.geometry as geometry

from datetime import datetime as dt

from pandas.api import types as pd_types

s3 = boto3.resource('s3')

def arcgis(data, job, bucket, object):
    log('converting raw data to GeoDataFrame')
    df = gpd.GeoDataFrame.from_features(data['features'])
    df.crs = {'init': 'epsg:4326'}

    log('parsing geometry to json strings')
    df['geometry'] = df['geometry'].apply(lambda x: geometry_to_record(x))

    transform(df, job, bucket, object)

def transform(data, job, bucket, object):
    if isinstance(data, (pd.DataFrame, gpd.GeoDataFrame)):
        pass

    # TODO: load in other formats of data as DataFrame

    log('validating data columns compared to the job config fields')
    data = data[[field['id'] for field in job['fields']]]

    for field in job['fields']:
        if field['type'] in ['bool', 'int', 'float']:
            data[field['id']] = data[field['id']].apply(
                lambda x: getattr(builtins, field['type'])(x) if not pd.isnull(x) else None
            )
        elif field['type'] in ['timestamp']:
            data[column] = data[column].apply(
                lambda x: datetime.utcfromtimestamp(x / 1000).strftime('%Y-%m-%d %H:%M:%S') if not pd.isnull(x) else None
            )

    log('saving transformed data to s3')
    buffer = io.StringIO()
    data.to_csv(buffer, index=False)

    s3.Bucket(bucket).put_object(Body=buffer.getvalue(), Key=object)

def lambda_handler(event, context):
    assert len(event['Records']) == 1, \
        build_response(500, 'Multiple records provided by input S3 event')

    storage = event['Records'][0].get('s3')

    bucket = storage['bucket']['name']
    object = storage['object']['key']

    try:
        log('fetching job config from s3')
        job_id = '-'.join(object.split('/')[-2].split('-')[3:])
        job = json.loads(get_object(bucket, f'jobs/{job_id}.json'))

        log('fetching extract output from s3')
        data = json.loads(get_object(bucket, object))
        next = build_path(object)

        globals()[job['transform']](data, job, bucket, next)

        log('job successfully completed')
    except Exception as e:
        print(e)
        return build_response(500, 'Something bad happened')

def build_path(object):
    fn, _ = os.path.splitext(object)

    return f'{fn.replace("extract/", "transform/")}.csv'

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

def geometry_to_record(row):
    if not row is None:
        row = geometry.mapping(row)

    return json.dumps(row)

def get_object(bucket, object):
    f = s3.Bucket(bucket).Object(object).get()

    return f['Body'].read()

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
        return 'unknown'

def log(msg):
    print(msg)
