import boto3
import pymysql
import pymssql
import snowflake.connector
import json
import os

s3 = boto3.client('s3')
ses = boto3.client('ses')

def lambda_handler(event, context):

    try:
        # ========= 1️⃣ READ FILE FROM S3 =========
        bucket = "api-s3-offline10"
        key = "api_data_.json"

        obj = s3.get_object(Bucket=bucket, Key=key)
        content = obj['Body'].read().decode('utf-8')
        data = json.loads(content)

        # ========= 2️⃣ INSERT INTO MYSQL =========
        mysql_conn = pymysql.connect(
            host=os.environ['pipelines3tomysql.c1w8km2uqjqp.ap-south-1.rds.amazonaws.com'],
            user=os.environ['admin'],
            password=os.environ['Admin#2025'],
            database="pipelines3tomysql"
        )

        mysql_cursor = mysql_conn.cursor()
        inserted_mysql = 0

        for row in data:
            try:
                mysql_cursor.execute("""
                    INSERT INTO Cust_data (userId, id, title, body)
                    VALUES (%s, %s, %s, %s)
                """, (
                    row['userId'],
                    row['id'],
                    row['title'],
                    row['body']
                ))
                inserted_mysql += 1

            except pymysql.err.IntegrityError:
                continue  # skip duplicates

        mysql_conn.commit()

        send_email("S3 → MySQL Success",
                   f"{inserted_mysql} records inserted into MySQL.")

        # ========= 3️⃣ MYSQL → MSSQL =========
        mysql_cursor.execute("SELECT userId, id, title, body FROM Cust_data")
        mysql_rows = mysql_cursor.fetchall()

        mssql_conn = pymssql.connect(
            server=os.environ['pipelines3tomssql.c1w8km2uqjqp.ap-south-1.rds.amazonaws.com'],
            user=os.environ['admin'],
            password=os.environ['Admin#2025'],
            database="pipelines3tomssql"
        )

        mssql_cursor = mssql_conn.cursor()
        inserted_mssql = 0

        for row in mysql_rows:
            try:
                cursor.execute(f"TRUNCATE TABLE {MSSQL_TABLE}")
                mssql_cursor.execute("""
                    INSERT INTO Cust_data (userId, id, title, body)
                    VALUES (%s, %s, %s, %s)
                """, row)
                inserted_mssql += 1
            except:
                continue

        mssql_conn.commit()

        send_email("MySQL → MSSQL Success",
                   f"{inserted_mssql} records moved to MSSQL.")

        # ========= 4️⃣ MSSQL → SNOWFLAKE =========
        mssql_cursor.execute("SELECT userId, id, title, body FROM Cust_data")
        mssql_rows = mssql_cursor.fetchall()

        snow_conn = snowflake.connector.connect(
            user=os.environ['HPMAHAJAN2013'],
            password=os.environ['4NH6idN4PNkM6Fb'],
            account=os.environ['GORPSJO-ZH89279'],
            warehouse=os.environ['COMPUTE_WH'],
            database=os.environ['PIPELINE_DB'],
            schema='PUBLIC'
        )

        

        snow_cursor = snow_conn.cursor()
        inserted_snow = 0

        for row in mssql_rows:
            try:
                snow_cursor.execute("""
                    INSERT INTO CUST_DATA (USERID, ID, TITLE, BODY)
                    VALUES (%s, %s, %s, %s)
                """, row)
                inserted_snow += 1
            except:
                continue

        snow_conn.commit()

        send_email("Pipeline Completed",
                   f"{inserted_snow} records loaded to Snowflake.")

        mysql_conn.close()
        mssql_conn.close()
        snow_conn.close()

        return {"status": "Pipeline Completed Successfully"}

    except Exception as e:
        send_email("Pipeline Failed", str(e))
        return {"status": "Failed", "error": str(e)}


def send_email(subject, message):

    ses.send_email(
        Source=os.environ['hpmahajan2013@gmail.com'],
        Destination={'ToAddresses': [os.environ['hpmahajan2013@gmail.com']]},
        Message={
            'Subject': {'Data': subject},
            'Body': {'Text': {'Data': message}}
        }
    )
