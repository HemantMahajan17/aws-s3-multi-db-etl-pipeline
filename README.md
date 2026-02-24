# AWS Data Pipeline

## Architecture

## 📌 End-to-End Data Flow

                ┌──────────────┐
                │ API Gateway  │
                └──────┬───────┘
                       ↓
                ┌──────────────┐
                │ Lambda (API) │
                └──────┬───────┘
                       ↓
                ┌──────────────┐
                │     S3       │
                └──────┬───────┘
                       ↓
                ┌──────────────┐
                │ Lambda (ETL) │
                └──────┬───────┘
                       ↓
        ┌────────────────────────────┐
        │           VPC              │
        │  ┌──────────────┐          │
        │  │   RDS MySQL  │          │
        │  └──────────────┘          │
        │  ┌──────────────┐          │
        │  │  RDS MSSQL   │          │
        │  └──────────────┘          │
        └────────────────────────────┘
                       ↓
                ┌──────────────┐
                │  Snowflake   │
                └──────────────┘
                       ↓
                ┌──────────────┐
                │     SES      │
                └──────────────┘

## Components

- API Lambda
- ETL Lambda
- MySQL (RDS)
- MSSQL (RDS)
- Snowflake
- SES

## Environment Variables Required

MYSQL_HOST  
MYSQL_USER  
MYSQL_PASSWORD  

MSSQL_HOST  
MSSQL_USER  
MSSQL_PASSWORD  

SNOW_USER  
SNOW_PASSWORD  
SNOW_ACCOUNT  
SNOW_WAREHOUSE  
SNOW_DB  

SENDER_EMAIL  
RECEIVER_EMAIL  

## Deployment Steps

1. Create RDS instances
2. Create S3 bucket
3. Create Lambda functions
4. Attach layers
5. Configure S3 trigger
6. Verify SES
