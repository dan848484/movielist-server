from typing import Mapping, Union, cast
import boto3
from MovieType import Movie
import uuid
import datetime
import json


def lambda_handler(event, context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("movielist-app")
    query = event["queryStringParameters"]
    if not query or "name" not in query:
        return {"statusCode": 400, "body": "query are not valid"}

    newItem: Movie = {
        "id": str(uuid.uuid4()),
        "name": query["name"],
        "addedDate": int(datetime.datetime.today().timestamp()),
        "watched": False,
    }
    print(query)
    response = table.put_item(Item=cast(Mapping[str, Union[int, bool, str]], newItem))

    return {
        "statusCode": 200,
        "body": json.dumps(newItem),
       
    }
