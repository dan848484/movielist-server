from decimal import Decimal
import json
from typing import cast
import boto3
from MovieType import Movie


def lambda_handler(event, context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("movielist-app")
    response = table.scan()
    data = response["Items"]
    while "LastEvaluatedKey" in response:
        response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        data.extend(response["Items"])

    for m in data:
        m["addedDate"] = int(cast(Decimal, m["addedDate"]))

    return {
        "statusCode": 200,
        "body": json.dumps(data),
    }
