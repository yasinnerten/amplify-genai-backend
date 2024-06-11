
#Copyright (c) 2024 Vanderbilt University  
#Authors: Jules White, Allen Karns, Karely Rodriguez, Max Moundas

import os
import json
import logging
from boto3.dynamodb.conditions import Key

from state import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')


def get(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response


def get_by_user(event, context):

  params = event['queryStringParameters']

  if not params or 'user' not in params:
    raise Exception("User not provided.")
    return

  user = params['user']

  table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

  # fetch all items for a specific user from the database
  result = table.query(
    IndexName='UserIndex',
    KeyConditionExpression=Key('user').eq(user)
  )

  # create a response
  response = {
    "statusCode": 200,
    "body": json.dumps(result['Items'], cls=decimalencoder.DecimalEncoder)
  }

  return response
