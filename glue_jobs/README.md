# Glue ETL Jobs

This directory contains three AWS Glue ETL jobs used in the YouTube data pipeline:

1. **youtube_cleaning_job**  
2. **complete_youtube_data_cleaning_job**  
3. **ETL_PIPELINE_cleaned_to_analytics**

---

## 1. youtube_cleaning_job (Python Shell)

- **Type**: Python shell script  
- **Location**: `glue_jobs/youtube_cleaning_job.py`  
- **Purpose**:  
  - Event-driven cleaning of a single region’s raw JSON file.  
- **Trigger**:  
  - S3 `ObjectCreated` events on bucket  
    `dataengineeringproject1-on-youtube-raw-useast1-dev`  
- **Input**:  
  - `s3://.../youtube/raw_statistics_reference_data/US_category_id.json`  
- **Logic**:  
  1. Read raw JSON from S3 using AWS Wrangler  
  2. Normalize the `items` array into tabular form  
  3. Write Parquet files to the cleansed S3 layer and update Glue catalog  
- **Output**:  
  - S3 path: `s3://...-fullcleaned-csv-to-parquet/youtube/cleaned_statistics/region=us/`  
  - Glue catalog DB: `db_youtube_cleaned`  
  - Glue catalog table: `cleaned_statistics_reference_data`  

---

## 2. complete_youtube_data_cleaning_job (Glue Script)

- **Type**: Scala/Python script (Script editor)  
- **Location**: `glue_jobs/complete_youtube_data_cleaning_job.py`  
- **Purpose**:  
  - Bulk-batch cleaning of **all regions’** raw data in one run.  
- **Trigger**:  
  - (Currently manual or via AWS CLI/Console)  
- **Input**:  
  - Glue catalog table `raw_statistics_reference_data` in `db_youtube_raw`  
- **Logic**:  
  1. Read dynamic frame from catalog (all partitions/regions)  
  2. Apply mappings, resolve choices, drop nulls, add metadata  
  3. Repartition by `region` and write Parquet  
- **Output**:  
  - S3 path: `s3://...-cleansed-useast1-dev/youtube/` partitioned by region  
  - Glue catalog DB: `db_youtube_cleaned`  
  - Glue catalog table: `cleaned_statistics_reference_data`  

---

## 3. ETL_PIPELINE_cleaned_to_analytics (Visual ETL)

- **Type**: Glue Studio Visual ETL job  
- **Job name**: `ETL_PIPELINE_cleaned_to_analytics`  
- **Purpose**:  
  - Join cleaned YouTube statistics with an analytics reference dataset and land results for BI/analytics.  
- **Data Sources**:  
  1. **Data Catalog** → Table: `cleaned_statistics_reference_data` in `db_youtube_cleaned`  
  2. **Data Catalog** → Table: `analytics_reference` in `dataengineering-analytics`  
- **Transform**:  
  - **Join** on  
    `cleaned_statistics_reference_data.id` = `analytics_reference.category_id`  
- **Data Target**:  
  - **Amazon S3** sink in Analytics bucket  
  - Output format: Parquet, partitioned by (e.g.) date or category  
- **Schedule**:  
  - (Configure under the **Schedules** tab in Glue Studio or via EventBridge)  
- **Version Control**:  
  - Enabled under **Version Control** tab  

---

**Next steps**  
- Configure **schedules/triggers** for the two batch jobs.  
- Review IAM permissions for each job’s role.  
- Add unit tests or sample runs in the **Runs** tab.  
