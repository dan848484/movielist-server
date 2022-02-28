from decimal import Decimal
import json
from typing import Any, Dict, List, cast
import boto3
from MovieType import Movie
import Add
import Delete
import Items
import Update


def lambda_handler(event, context):
    operation: str = event["pathParameters"]["operation"]
    operationFunctions = {
        "items": Items.lambda_handler,
        "add": Add.lambda_handler,
        "delete": Delete.lambda_handler,
        "update": Update.lambda_handler,
    }
    response = None

    for o in operationFunctions:
        if o == operation:
            response = operationFunctions[o](event, context)
            break

    return response
