from datetime import datetime
import logging
import boto3
from datetime import datetime


ENDPOINT = "arn:aws:dynamodb:us-east-1:552644432618:table/JeepTrails"
TABLE_NAME = "JeepTrails"

#Defining function to put item in dynamodb table
def PutItem(TrailName, TrailDiff):

    try:
        db_client = boto3.client("dynamodb")
        db_client.put_item(
            Item={
                "TrailName": {
                    "S": TrailName,
                },
                "TrailDiff": {
                    "S": TrailDiff,
                },
            },
            ReturnConsumedCapacity="TOTAL",
            TableName=TABLE_NAME,
        )
        return True
    except Exception as e:
        logging.error(e)
        return False


#Defining the lambda function
def lambda_handler(event, context):


    TrailName = "Rubicon"
    TrailDiff = "Hard"
    if PutItem(TrailName, TrailDiff):
        return {"statusCode": 200, "body": "Item successfully put in"}

    return {"statusCode": 400, "body": "Error putting item in"}


#Test Main for Debugging
if __name__ == "__main__":
    lambda_handler(None, None)
