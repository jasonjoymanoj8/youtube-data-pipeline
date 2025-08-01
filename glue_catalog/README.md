# AWS Glue Data Catalog

The AWS Glue Data Catalog is the central metadata store for all of the datasets in our YouTube analytics pipeline.  It provides:

- **Unified schema definitions** for all data sources and sinks.  
- **Discoverability**: Athena, Glue ETL jobs, and other services can easily look up table definitions.  
- **Versioning** and **data quality** features to track how schemas evolve over time.

This directory documents the four Glue Catalog _databases_ used by our pipeline, and the key _tables_ in each.

---

## 1. `dataengineering-youtube-raw`

**Purpose**: Landing zone for raw exports from the YouTube API.

| Table                              | Format | Location                                                                      | Notes                                                                                                 |
|------------------------------------|--------|-------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| `raw_statistics_reference_data`    | JSON   | `s3://…/youtube/raw_statistics_reference_data/`                                | Static category lookup data (e.g. channel & video metadata).                                          |
| `raw_statistics`                   | CSV    | `s3://…/youtube/raw_statistics/`                                              | Daily trending statistics per video, one file per region before any normalization or parsing.         |

---

## 2. `db_youtube_cleaned`

**Purpose**: Structured, normalized Parquet tables produced by our event-driven Lambda and full cleaning jobs.

| Table                                    | Format  | Location                                                                  | Notes                                                                                          |
|------------------------------------------|---------|---------------------------------------------------------------------------|------------------------------------------------------------------------------------------------|
| `cleaned_statistics_reference_data`      | Parquet | `s3://…/youtube/cleaned_statistics_reference_data/`                       | Flattened version of the JSON lookup, used as a dimension table.                              |
| `cleaned_statistics`                     | Parquet | `s3://…/youtube/cleaned_statistics/`                                      | Core fact table of daily trending stats, partitioned by `region`.                             |

---

## 3. `db_youtube_analytics`

**Purpose**: Final, enriched analytics tables ready for ad-hoc query in Athena or BI tools.

| Table               | Format  | Location                                                   | Notes                                                                                     |
|---------------------|---------|------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| `final_analytics`   | Parquet | `s3://dataengineering-analytics/`                          | Join of cleaned facts + reference data with additional derived metrics and date dimensions. |

---

## 4. `default`

This is the built-in Glue “default” database. We do _not_ use it for any of our pipeline datasets.

---

## How It All Fits Together

1. **Raw** data lands under `dataengineering-youtube-raw`  
2. **Lambda** and **Glue ETL** cleaning jobs write Parquet into `db_youtube_cleaned`  
3. A final **Glue Studio** job joins and enriches into `db_youtube_analytics`  
4. **Athena** points at `db_youtube_analytics` for reporting and exploration  

By centralizing all schema definitions in the Glue Data Catalog, we ensure every consumer (ETL, Athena, QuickSight, etc.) sees the same up-to-date table structure.  
