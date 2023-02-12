from decimal import Decimal
from json import dumps, loads
from typing import Mapping, Union, cast
from MovieType import Movie
import uuid
import datetime
from distutils.util import strtobool
import boto3
from mypy_boto3_dynamodb import ServiceResource

def lambda_handler(event, context):
    method:str = event['httpMethod']
    response:object = None
    try:
        if method == "GET":
            response = get_movies(event,context)
        elif method == "POST":
            response = add_movie(event,context)
        elif method == "PUT":
            response = update_movie(event,context)
        elif  method == 'DELETE':
            response = delete_movie(event,context)   
        return {
            'statusCode':200,
            'body':dumps(response)
        }
    except EmptyBodyError as ex:
        return {
            'statusCode':400,
            'body':ex.__str__()
        }
    except Exception as ex:
        return {
            'statusCode':500,
            'body':ex.__str__()
        }
    

def get_movies(event, context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("movielist-app")
    response = table.scan()
    data = response["Items"]
    while "LastEvaluatedKey" in response:
        response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        data.extend(response["Items"])

    for m in data:
        m["addedDate"] = int(cast(Decimal, m["addedDate"]))

    return data

def add_movie(event, context):
    dynamodb:ServiceResource = boto3.resource("dynamodb")
    table = dynamodb.Table("movielist-app")
    body:Movie = loads(event['body'])
    print(type(body))
    if body is None:
        raise EmptyBodyError()
    newItem: Movie = {
        "id": str(uuid.uuid4()),
        "name": body['name'],
        "addedDate": int(datetime.datetime.today().timestamp()),
        "watched": False,
    }
    table.put_item(Item=cast(Mapping[str, Union[int, bool, str]], newItem))
    return newItem

def update_movie(event, context):
    dynamodb:ServiceResource = boto3.resource("dynamodb")
    table = dynamodb.Table("movielist-app")
    body:Movie = loads(event['body'])
    if body is None:
        raise EmptyBodyError()
    table.update_item(
        Key={"id": body["id"]},
        UpdateExpression="SET #movie_name = :movie_name, addedDate = :date, watched = :watched",
        ExpressionAttributeValues={
            ":movie_name": body['name'],
            ":date":body['addedDate'],
            ":watched":True if strtobool(str(body["watched"])) else False
        },
        ExpressionAttributeNames={
            '#movie_name':'name'
        }
    )
    updatedItem = table.get_item(Key={
        'id':body["id"],
    })["Item"] 
    updatedItem["addedDate"] = int(cast(Decimal,updatedItem["addedDate"]))
    return updatedItem


def delete_movie(event, context):
    dynamodb:ServiceResource = boto3.resource("dynamodb")
    table = dynamodb.Table("movielist-app")
    id: str = event["pathParameters"]["id"]
    table.delete_item(Key={"id": id})
    return None

class EmptyBodyError(Exception):
    def __init__(self):
        super().__init__("Bodyがありません。")
