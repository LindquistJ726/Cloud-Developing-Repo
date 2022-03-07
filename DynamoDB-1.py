#Joshua Lindquist
#Assignment: DynamoDB Table
#Description: This program will create, load, pull from, and delete a table.

import logging
import time
import boto3
from botocore.exceptions import ClientError
TABLE_NAME = 'JeepTrails'
INDEX_NAME_JT = 'JTrailIndex'
INDEX_NAME_DIFF = 'DiffIndex'

#Defining the function to create the table

def make_table(db_client):
    try:
        db_client.create_table(
          AttributeDefinitions=[
             {
                  'AttributeName': 'TrailNum',
                  'AttributeType': 'S',
              },
              {
                  'AttributeName': 'Difficulty',
                  'AttributeType': 'S',
              },
              {
                  'AttributeName': 'TrailTraveled',
                  'AttributeType': 'B',
              }
          ],
          KeySchema=[
              {
                  'AttributeName': 'TrailNum',
                  'KeyType': 'HASH',
              },
              {
                  'AttributeName': 'Difficulty',
                  'KeyType': 'RANGE',
              }
          ],
          ProvisionedThroughput={
              'ReadCapacityUnits': 2,
              'WriteCapacityUnits': 2,
          },
          GlobalSecondaryIndexes=[
          {
                'IndexName': INDEX_NAME_JT,
                'KeySchema': [
                    {
                        'AttributeName': 'Difficulty',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'TrailNum',
                        'KeyType': 'RANGE'
                    },
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 2,
                    'WriteCapacityUnits': 2
                }
            },
            {
                'IndexName': INDEX_NAME_DIFF,
                'KeySchema': [
                    {
                      'AttributeName': 'Difficulty',
                      'KeyType': 'HASH'
                    },
                    {
                      'AttributeName': 'TrailTraveled',
                      'KeyType': 'RANGE'
                    },
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 2,
                    'WriteCapacityUnits': 2
                }
            },
          ],
          TableName=TABLE_NAME,
        )
        return True
    except ClientError as e:
        logging.error(e)
        return False
#Creating a function to describe the table
def describe_table():
    try:
        db_client = boto3.client('dynamodb')
        response = db_client.describe_table(TableName=TABLE_NAME)
        return response['Table']['TableStatus']
    except ClientError as e:
        logging.error(e)
        return None
#Creating a function to load the table
def put_item(TrailNum,Difficulty,Name,Description,Location,TrailTraveled):
    ENDPOINT = 'http://localhost:8000'
    db_client = boto3.client('dynamodb', endpoint_url=ENDPOINT)
    db_client.put_item(
        Item={
          'TrailNum': {
            'S': TrailNum,
          },
          'Difficulty': {
            'S': Difficulty,
          },
          'Name': {
            'S': Name,
          },
          'Description': {
            'S': Description,
          },
          'Location': {
            'S': Location,
          },
          'TrailTraveled': {
            'B': TrailTraveled
          },
        },
        ReturnConsumedCapacity='TOTAL',
        TableName=TABLE_NAME,
      )
#Creating function to pull items from the table 
def Get_Item(TrailNum,Difficulty):
    ENDPOINT = 'http://localhost:8000'
    db_client = boto3.client('dynamodb', endpoint_url=ENDPOINT)
    response = db_client.get_item(
        Key={
          'TrailNum': {
            'S': TrailNum,
          },
          'Difficulty': {
              'S': Difficulty,
          },      
        },
        TableName=TABLE_NAME,
    )
#Creating the function that will delete items from the table
def Delete_Item(TrailNum,Difficulty):
    ENDPOINT = 'http://localhost:8000'
    db_client = boto3.client('dynamodb', endpoint_url=ENDPOINT)
    response = db_client.delete_item(
    TableName=TABLE_NAME,
    Key={
        'TrailNum': [
             TrailNum ,
        ],
          'Difficulty': [
               Difficulty,
          ]
        }   
    )
#Function to delete the table
def Delete_table(TABLE_NAME):
     ENDPOINT = 'http://localhost:8000'
     db_client = boto3.client('dynamodb', endpoint_url=ENDPOINT)
     db_client.delete_table(TableName=TABLE_NAME)
    
def main():
  ENDPOINT = 'http://localhost:8000'
  db_client = boto3.client('dynamodb', endpoint_url=ENDPOINT)

  #Calling the function to make the take, and pause it during its creation
  make_table(db_client)
  while True:
    results = describe_table()
    if results == 'ACTIVE':
      break
    time.sleep(5)
#Adding three different trails to the table
  put_item('JT1','Hard','Rubicon Trail', 'A famous benchmark trail','California','False')
  put_item('JT2','Medium','Drummond Island', 'A Jeep Jamboree Location in northern Michigan','Michigan','False')
  put_item('JT3','Easy','St. Helen Trail', 'A Popular Mid-Michigan Trail','Michigan','True')
#Adding three more with the secondary index
  put_item('JC1','Easy','BadLands', 'A Course that Provides easy to extreme trails','Indiana','False')
  put_item('JC2','Expert','Moab Course', 'A famous group of trails used in conjuction to the Rubicon trail for benchmarking','Utah','False')
  put_item('JC3','Medium','Big Bear', 'A former gold mining area turned into a multiple Jeep trails','California','False')
#Using the Get_Item function to pull an item from the table
  item = Get_Item('JT2',"Medium") 
  print('Trail:', item)
  Delete_table(TABLE_NAME)

#Calling main
main()