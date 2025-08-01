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


# Amazon Athena

This directory documents how we use Amazon Athena to run ad-hoc SQL queries over our Glue-cataloged YouTube data.

## 1. Setup

- **Data source:** AwsDataCatalog  
- **Workgroup:** primary  
- **Databases in Catalog:**
  - `dataengineering-youtube-raw` (raw JSON/CSV tables)
  - `db_youtube_cleaned`    (cleaned Parquet tables)
  - `db_youtube_analytics`  (final analytics table)

You first select the database from the left-hand pane, then begin typing your SQL in the editor.

---

## 2. Sample Queries

Below are the core patterns you’ll use frequently. You can copy the entire block and run each one by uncommenting its `SELECT` statement.

```sql
-- 2.1 List some reference lookup rows
-- SELECT * 
--   FROM "AwsDataCatalog"."db_youtube_cleaned"."cleaned_statistics_reference_data"
--   LIMIT 10;

-- 2.2 Filter raw facts by region (e.g., Canada)
-- SELECT *
--   FROM "AwsDataCatalog"."dataengineering-youtube-raw"."raw_statistics"
--   WHERE region = 'ca';

-- 2.3 Join raw facts to lookup for US videos
-- SELECT
--     a.video_id,
--     a.title,
--     b.snippet_title AS category_name
--   FROM "AwsDataCatalog"."dataengineering-youtube-raw"."raw_statistics" a
--   INNER JOIN "AwsDataCatalog"."db_youtube_cleaned"."cleaned_statistics_reference_data" b
--     ON a.category_id = b.id
--   WHERE a.region = 'us';

-- 2.4 Aggregate daily views by category
-- SELECT
--     b.snippet_title AS category_name,
--     SUM(a.views) AS total_views
--   FROM "AwsDataCatalog"."db_youtube_cleaned"."cleaned_statistics" a
--   INNER JOIN "AwsDataCatalog"."db_youtube_cleaned"."cleaned_statistics_reference_data" b
--     ON a.category_id = b.id
--   GROUP BY b.snippet_title
--   ORDER BY total_views DESC
--   LIMIT 10;

-- 2.5 Query the final analytics table
-- SELECT *
--   FROM "AwsDataCatalog"."db_youtube_analytics"."final_analytics"
--   WHERE trending_date BETWEEN date '2025-07-01' AND date '2025-07-31'
--   ORDER BY likes DESC
--   LIMIT 25;

