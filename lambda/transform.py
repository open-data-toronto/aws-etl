import builtins
import datatime.datetime as dt
import io
import json

import boto3
import geopandas as gpd
import numpy as np
import pandas as pd
import shapely.geometry as geometry

s3 = boto3.resource('s3')

def geometry_to_record(row):
    if not row is None:
        row = geometry.mapping(row)

    return json.dumps(row)

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

def arcgis(data, job, bucket, object):
    df = gpd.read_file(data)
    df.crs = {'init': 'epsg:4326'}

    df['geometry'] = df['geometry'].apply(lambda x: geometry_to_record(x))

    transform(df, job, bucket, object)

def transform(data, job, bucket, object):
    if isinstance(data, (pd.DataFrame, gpd.GeoDataFrame)):
        continue

    # TODO: load in other formats of data as DataFrame

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

    buffer = io.StringIO()
    data.to_csv(buffer, index=False)

    s3.put_object(Body=buffer.getvalue(), Bucket=bucket, Key=next)

def lambda_handler(event, context):
    assert len(event['Records']) == 0, \
        build_response(500, 'Multiple records provided by input S3 event')

    storage = event['Records'][0].get('s3')

    bucket = storage['bucket']['name']
    object = storage['object']['key']

    try:
        job_id = '-'.join(object.split('/')[-2].split('-')[1:])
        job = json.loads(get_object(bucket, f'/jobs/{job_id}.json'))

        data = io.BytesIO(get_object(bucket, object))
        next = build_path(object)

        globals()[job['transform']](data, job, bucket, next)
    except:
        return build_response(500, 'Something bad happened')

def build_path(object):
    fn, _ = os.path.splitext(object)

    return f'{fn.replace('/extract/', '/transform/')}.csv'

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
