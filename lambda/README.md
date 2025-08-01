# youtube_cleaning_event_lambda

This AWS Lambda function is triggered by S3 **ObjectCreated** events on the `dataengineeringproject1-on-youtube-raw-useast1-dev` bucket.  
When a new JSON file lands, it:
1. Reads the raw JSON from S3.
2. Normalizes the `"items"` array into a Pandas DataFrame.
3. Writes the cleaned DataFrame to the Cleansed S3 layer in Parquet format.
4. Registers the data in the Glue Data Catalog (`db_youtube_cleaned.cleaned_statistics_reference_data`).

## Configuration

- **Trigger bucket:** `dataengineeringproject1-on-youtube-raw-useast1-dev`
- **Environment variables:**
  - `S3_CLEANSED_LAYER` &rarr; S3 path for Parquet output
  - `GLUE_CATALOG_DB_NAME` &rarr; Glue database name
  - `GLUE_CATALOG_TABLE_NAME` &rarr; Glue table name
  - `WRITE_DATA_OPERATION` &rarr; write mode (`append`)

## Usage

Deploy this function and ensure it has:
- An S3 trigger on `ObjectCreated:*`
- Permissions to read source bucket, write target bucket, and update Glue.

## Known limitation: AWSDataWrangler dependency & trigger

**What’s broken:**  
- The Lambda function currently fails with `No module named 'awswrangler'`.  
- Because we can’t add the AWS Data Wrangler layer in this region, the function can’t load the `awswrangler` library at runtime.  
- As a result, even though the S3-bucket trigger is configured, the handler never runs successfully.

**Why it happens:**  
- AWS publishes an AWSDataWrangler layer only in certain regions.  
- In regions where that layer ARN isn’t available (like us-east-1 for our account), Lambda can’t pull in the library.  
- Without `awswrangler`, the code errors out before writing to Glue/S3.

**Workaround / Next steps:**  
1. Package `awswrangler` and its dependencies into a custom Lambda layer (or include it in your deployment bundle).  
2. Attach that custom layer under **Layers** in the function’s Configuration tab.  
3. Re-deploy, and then the S3 “ObjectCreated” trigger will successfully invoke the handler.  
