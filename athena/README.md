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
