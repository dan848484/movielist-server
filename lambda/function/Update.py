from typing import Union
import boto3
from distutils.util import strtobool


def lambda_handler(event, context):

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("movielist-app")
    query = event["queryStringParameters"]
    if not query or "id" not in query or "type" not in query or "value" not in query:
        return {"statusCode": 400, "body": "query are not valid"}

    type: str = query["type"]
    value: Union[str, bool] = query["value"]
    if not (type in {"name", "watched"}):
        return {"statusCode": 400, "body": " 'type' query is not valid"}
    if not value:
        return {"statusCode": 400, "body": "'value' query is not specified"}

    if type == "watched":
        try:
            value = True if strtobool(str(value)) else False
        except ValueError as e:
            return {
                "statusCode": 400,
                "body": "'value' query is not valid. this is error message \n "
                + e.__str__(),
            }

    table.update_item(
        Key={"id": query["id"]},
        UpdateExpression="SET #type = :val",
        ExpressionAttributeValues={":val": value},
        ExpressionAttributeNames={"#type": type},
    )

    return {
        "statusCode": 200,
        "body": "changed " + type + " to " + query["id"],
    }
