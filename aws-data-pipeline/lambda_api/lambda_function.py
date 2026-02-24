import json
import boto3
import urllib.request
from datetime import datetime
import os

s3 = boto3.client('s3')

BUCKET_NAME = os.environ['BUCKET_NAME']

def lambda_handler(event, context):

    try:
        url = "https://jsonplaceholder.typicode.com/posts"

        # Call external API
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())

        file_name = f"api_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=f"raw/{file_name}",
            Body=json.dumps(data),
            ContentType="application/json"
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "File uploaded to S3 successfully",
                "file": file_name
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }