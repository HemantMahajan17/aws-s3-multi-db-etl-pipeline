<<<<<<< HEAD
# AWS Data Pipeline

## Architecture

API → Lambda → S3  
S3 Trigger → Lambda  
MySQL → MSSQL → Snowflake  
SES Notifications  

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
=======
# AWS Data Pipeline

## Architecture

API → Lambda → S3  
S3 Trigger → Lambda  
MySQL → MSSQL → Snowflake  
SES Notifications  

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
>>>>>>> 26b5ae4924b9e1eeec3e5d462ff58810aecb59bd
6. Verify SES