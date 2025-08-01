import awswrangler as wr
import pandas as pd
import urllib.parse
import os

# read exactly the env-var names you defined in the console
s3_cleansed_layer       = os.environ['S3_CLEANSED_LAYER']
glue_catalog_db_name    = os.environ['GLUE_CATALOG_DB_NAME']
glue_catalog_table_name = os.environ['GLUE_CATALOG_TABLE_NAME']
write_data_operation    = os.environ['WRITE_DATA_OPERATION']

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key    = urllib.parse.unquote_plus(
                 event['Records'][0]['s3']['object']['key'],
                 encoding='utf-8'
             )

    try:
        # 1) read the new JSON
        df_raw = wr.s3.read_json(f's3://{bucket}/{key}')

        # 2) normalize the items list into columns
        df_step_1 = pd.json_normalize(df_raw['items'])

        # 3) write to your cleansed S3 / Glue catalog
        wr_response = wr.s3.to_parquet(
            df=df_step_1,
            path=s3_cleansed_layer,
            dataset=True,
            database=glue_catalog_db_name,
            table=glue_catalog_table_name,
            mode=write_data_operation
        )

        return wr_response

    except Exception as e:
        print(f"Error processing s3://{bucket}/{key}: {e}")
        raise
