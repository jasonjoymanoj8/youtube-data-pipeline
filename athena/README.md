# Amazon Athena

This directory documents how we use **Amazon Athena** to run ad-hoc SQL queries over our YouTube data (backed by the Glue Data Catalog).

---

## 1. Configuration

- **Data source**: `AwsDataCatalog`  
- **Workgroup**: `primary` (default)  
- **Query results location**: configured in the Athena console (e.g. `s3://<your-bucket>/aws-athena-query-results/`)

---

## 2. Databases

We expose three Glue databases in Athena:

| Database                        | Purpose                                                                  |
|---------------------------------|--------------------------------------------------------------------------|
| `dataengineering-youtube-raw`   | Raw JSON & CSV landing tables (region-partitioned raw statistics + lookup data) |
| `db_youtube_cleaned`            | Parquet tables produced by our event-driven Lambda & Glue ETL jobs      |
| `db_youtube_analytics`          | Final, enriched analytics tables ready for BI tools and dashboards       |

---
## 3. Common Queries

### 3.1 Preview the reference lookup table
```sql
SELECT *
FROM "AwsDataCatalog"."db_youtube_cleaned"."cleaned_statistics_reference_data"
LIMIT 10;

-- 3.2 Filter raw facts by region
SELECT *
FROM "AwsDataCatalog"."dataengineering-youtube-raw"."raw_statistics"
WHERE region = 'ca';

-- 3.3 Join raw facts to lookup for US videos
SELECT
  a.video_id,
  a.title,
  b.snippet_title AS category_name,
  a.views,
  a.likes
FROM "AwsDataCatalog"."dataengineering-youtube-raw"."raw_statistics" AS a
JOIN "AwsDataCatalog"."db_youtube_cleaned"."cleaned_statistics_reference_data" AS b
  ON a.category_id = b.id
WHERE a.region = 'us';

-- 3.4 (Re)create the analytics database
CREATE DATABASE IF NOT EXISTS db_youtube_analytics;

-- 3.5 Query the final analytics table
SELECT *
FROM "AwsDataCatalog"."db_youtube_analytics"."final_analytics"
LIMIT 100;

SELECT *
FROM "AwsDataCatalog"."db_youtube_cleaned"."cleaned_statistics_reference_data"
LIMIT 10;
