import boto3


def lambda_handler(event, context):

    dynamodb = boto3.resource("dynamodb")

    table = dynamodb.Table("movielist-app")
    query = event["queryStringParameters"]
    if not query or "id" not in query:
        return {"statusCode": 400, "body": "query are not valid"}

    response = table.delete_item(Key={"id": query["id"]})

    return {
        "statusCode": 200,
        "body": "deleted: " + query["id"],
        # "body": "test",
    }
