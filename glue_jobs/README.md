# Glue ETL Jobs

This directory contains three AWS Glue ETL jobs used in the YouTube data pipeline:

1. **youtube_cleaning_job**  
2. **complete_youtube_data_cleaning_job**  
3. **ETL_PIPELINE_cleaned_to_analytics**  

---

## 1. youtube_cleaning_job (Python shell)

- **Type**: Python shell script  
- **Location**: `glue_jobs/youtube_cleaning_job.py`  
- **Purpose**:  
  - Event-driven cleaning of a single region’s raw JSON file.  

- **Trigger**:  
  - S3 `ObjectCreated` events on bucket `dataengineeringproject1-on-youtube-raw-useast1-dev`  

- **Input**:  
  - `s3://…/youtube/raw_statistics_reference_data/US_category_id.json`  

- **Logic**:  
  1. Read raw JSON from S3 using AWS Wrangler  
  2. Normalize the `items` list into a flat table using `pandas.json_normalize`  
  3. Write Parquet to the cleansed S3 location and register partitions in Glue Data Catalog  

- **Output**:  
  - Parquet files in `s3://dataengineeringproject1-on-youtube-fullcleaned-csv-to-parquet/youtube/cleaned_statistics/region=us/`  
  - Glue table `db_youtube_cleaned.cleaned_statistics_reference_data` updated  

---

## 2. complete_youtube_data_cleaning_job (Glue ETL script)

- **Type**: Scala/Python ETL script (script editor)  
- **Location**: `glue_jobs/complete_youtube_data_cleaning_job.scala` (or `.py`)  
- **Purpose**:  
  - Batch processing: cleans and enriches multiple regions’ JSON files in one job.  

- **Trigger**:  
  - Manually scheduled or invoked via AWS Step Functions  

- **Inputs**:  
  - All JSON files under `s3://dataengineeringproject1-on-youtube-raw-useast1-dev/youtube/raw_statistics_reference_data/`  

- **Logic**:  
  1. Read all JSONs into a DynamicFrame  
  2. Apply data cleaning transforms (drop nulls, cast types, enrich columns)  
  3. Write out partitioned Parquet to S3 and update the Glue Catalog  

- **Output**:  
  - Parquet dataset in `s3://dataengineeringproject1-on-youtube-cleansed-useast1-dev/youtube/`  
  - Glue table `db_youtube_cleaned.cleaned_statistics`  

---

## 3. ETL_PIPELINE_cleaned_to_analytics (Glue Studio Visual ETL)

- **Type**: Visual ETL (Glue Studio)  
- **Location**: defined in the Glue Studio UI under **ETL_PIPELINE_cleaned_to_analytics**  
- **Purpose**:  
  - Join cleaned statistics with reference data (e.g. category names) and write to analytics layer.  

- **Trigger**:  
  - Scheduled or manually run from the Glue Studio console  

- **Inputs**:  
  1. **Cleaned statistics** table from Glue Catalog (`db_youtube_cleaned.cleaned_statistics_reference_data`)  
     ![Data source 1 screenshot](../assets/glue_job3_source1.png)  
  2. **Reference data** table from Glue Catalog (`db_youtube_cleaned.cleaned_statistics`)  
     ![Data source 2 screenshot](../assets/glue_job3_source2.png)  

- **Transform**:  
  - **Join** on `id = category_id`  
    ![Join node screenshot](../assets/glue_job3_join.png)  

- **Output**:  
  - Data target: Amazon S3  
    ![Data target screenshot](../assets/glue_job3_target.png)  
  - Writes enriched Parquet to `s3://dataengineeringproject1-on-youtube-analytics/`  
  - (Optional) updates a Glue table `db_youtube_analytics.youtube_statistics`  

---

### Notes

- Screenshots are stored in `assets/` so you can reference them in this README.  
- Adjust paths, database & table names as needed if you promote from dev to prod.  
