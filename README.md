# AWS Data Pipeline: S3 → RDS MySQL → RDS MSSQL → Snowflake

## Overview

This project implements an **automated serverless data pipeline** using AWS services and Snowflake.

The pipeline reads JSON data from **Amazon S3**, loads it into **Amazon RDS MySQL**, transfers it to **Amazon RDS SQL Server**, and finally loads it into **Snowflake** for analytics.

The entire workflow runs inside an **AWS Lambda function** triggered by S3 events.

---

# Architecture


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



# Technologies Used

* AWS Lambda
* Amazon S3
* Amazon RDS (MySQL)
* Amazon RDS (SQL Server)
* Snowflake
* Python 3.12
* Boto3
* PyMySQL
* PyMSSQL
* Snowflake Connector

---

# Project Workflow

1. JSON file uploaded to S3.
2. Lambda function reads the file.
3. Data inserted into **RDS MySQL**.
4. Data transferred from **MySQL → MSSQL**.
5. Data loaded from **MSSQL → Snowflake**.
6. Email notification sent using **AWS SES**.

---

# Lambda Dependencies

The Lambda function requires the following Python libraries:

* snowflake-connector-python
* pymysql
* pymssql
* cryptography

Because these libraries are not included in AWS Lambda by default, we create a **Lambda Layer**.

---

# Creating Snowflake Lambda Layer (Python 3.12)

## Step 1 — Connect to EC2

```bash
ssh -i your-key.pem ubuntu@EC2_PUBLIC_IP
```

---

## Step 2 — Install Dependencies

```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3-pip zip unzip -y
```

---

## Step 3 — Create Project Directory

```bash
mkdir snowflake_layer
cd snowflake_layer
```

---

## Step 4 — Create Virtual Environment

```bash
python3.12 -m venv venv
source venv/bin/activate
```

---

## Step 5 — Upgrade pip

```bash
pip install --upgrade pip
```

---

## Step 6 — Create Lambda Layer Structure

```bash
mkdir -p python/lib/python3.12/site-packages
```

Required structure:

```
python/lib/python3.12/site-packages/
```

---

## Step 7 — Install Required Packages

```bash
pip install snowflake-connector-python pymysql pymssql cryptography \
-t python/lib/python3.12/site-packages/
```

---

## Step 8 — Create ZIP File

```bash
zip -r snowflake_lambda_layer.zip python
```

---

## Step 9 — Verify ZIP

```bash
unzip -l snowflake_lambda_layer.zip
```

Expected structure:

```
python/lib/python3.12/site-packages/snowflake
python/lib/python3.12/site-packages/pymysql
python/lib/python3.12/site-packages/pymssql
```

---

# Upload Layer to AWS

## Configure AWS CLI

```bash
pip install awscli
aws configure
```

---

## Upload Layer

```bash
aws lambda publish-layer-version \
--layer-name snowflake-layer \
--zip-file fileb://snowflake_lambda_layer.zip \
--compatible-runtimes python3.12
```

AWS will return a **Layer ARN**.

Example:

```
arn:aws:lambda:ap-south-1:123456789012:layer:snowflake-layer:1
```

---

# Attach Layer to Lambda

AWS Console:

```
Lambda → Function → Layers → Add Layer → snowflake-layer
```

---

# Lambda Configuration

Recommended settings:

Memory:

```
512 MB
```

Timeout:

```
30 seconds
```

Runtime:

```
Python 3.12
```

---

# Environment Variables

Configure Lambda environment variables:

```
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
```

---

# Example Snowflake Connection

```python
snow_conn = snowflake.connector.connect(
    user=os.environ['SNOW_USER'],
    password=os.environ['SNOW_PASSWORD'],
    account=os.environ['SNOW_ACCOUNT'],
    warehouse=os.environ['SNOW_WAREHOUSE'],
    database=os.environ['SNOW_DB'],
    schema='PUBLIC'
)
```

---

# Future Improvements

* Implement incremental loading
* Add Airflow orchestration
* Use AWS Secrets Manager
* Add monitoring using CloudWatch

---

# Author

Hemant Mahajan
