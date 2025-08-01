# IAM Roles & Policies

This folder documents the IAM roles and policies that power the YouTube data pipeline, granting least-privilege access to each AWS service.

---

## 1. `youtube_cleaning_event_lambda_role`

**Trust relationship**  
Allows the Lambda service (`lambda.amazonaws.com`) to assume this role.

**Purpose**  
- Triggered on S3 `ObjectCreated` events in the **raw JSON** bucket.  
- Reads raw JSON files.  
- Writes cleaned Parquet to the **cleansed** bucket.  
- Emits logs/metrics to CloudWatch.

**Attached policies**  
- **AWS managed**  
  - `AWSLambdaBasicExecutionRole` (CloudWatch Logs)
- **Inline custom policy**  
  ```json
  {
    "Version":"2012-10-17",
    "Statement":[
      {
        "Effect":"Allow",
        "Action":[
          "s3:GetObject",
          "s3:ListBucket"
        ],
        "Resource":[
          "arn:aws:s3:::dataengineeringproject1-on-youtube-raw-useast1-dev",
          "arn:aws:s3:::dataengineeringproject1-on-youtube-raw-useast1-dev/*"
        ]
      },
      {
        "Effect":"Allow",
        "Action":"s3:PutObject",
        "Resource":"arn:aws:s3:::dataengineeringproject1-on-youtube-fullcleaned-csv-to-parquet/*"
      }
    ]
  }
