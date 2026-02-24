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
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']

        obj = s3.get_object(Bucket=bucket, Key=key)
        content = obj['Body'].read().decode('utf-8')
        data = json.loads(content)

        # ========= 2️⃣ INSERT INTO MYSQL =========
        mysql_conn = pymysql.connect(
            host=os.environ['MYSQL_HOST'],
            user=os.environ['MYSQL_USER'],
            password=os.environ['MYSQL_PASSWORD'],
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
            server=os.environ['MSSQL_HOST'],
            user=os.environ['MSSQL_USER'],
            password=os.environ['MSSQL_PASSWORD'],
            database="pipelines3tomssql"
        )

        mssql_cursor = mssql_conn.cursor()
        inserted_mssql = 0

        for row in mysql_rows:
            try:
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
            user=os.environ['SNOW_USER'],
            password=os.environ['SNOW_PASSWORD'],
            account=os.environ['SNOW_ACCOUNT'],
            warehouse=os.environ['SNOW_WAREHOUSE'],
            database=os.environ['SNOW_DB'],
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
        Source=os.environ['SENDER_EMAIL'],
        Destination={'ToAddresses': [os.environ['RECEIVER_EMAIL']]},
        Message={
            'Subject': {'Data': subject},
            'Body': {'Text': {'Data': message}}
        }
    )