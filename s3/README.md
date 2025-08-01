# S3 Buckets

This directory documents the S3 buckets used by the YouTube data pipeline.

---

## 1. Raw JSON Landing Bucket

- **Name**: `dataengineeringproject1-on-youtube-raw-useast1-dev`  
- **Region**: `us-east-1`  
- **Purpose**:  
  - Receives raw JSON files exported from the YouTube API.  
  - **Triggers** the `youtube_cleaning_event_lambda` on every `ObjectCreated` event.  

---

## 2. Cleansed Parquet Bucket

- **Name**: `dataengineeringproject1-on-youtube-fullcleaned-csv-to-parquet`  
- **Region**: `us-east-1`  
- **Purpose**:  
  - Stores the cleaned, normalized data in Parquet format.  
  - Populated by the Lambda function and cataloged in AWS Glue.  

---

## 3. Analytics / Reporting Bucket

- **Name**: `dataengineering-analytics`  
- **Region**: `us-east-1`  
- **Purpose**:  
  - Holds joined, aggregated, or otherwise transformed datasets ready for business reporting.  
  - Queried via Athena for dashboards and ad-hoc analysis.  
