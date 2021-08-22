import json
import os
from typing import Dict, Any

import boto3

# https://github.com/boto/botocore/issues/2218
api_gateway_management_api_client = boto3.client(
    "apigatewaymanagementapi", endpoint_url=os.environ["EXECUTE_API_ENDPOINT"]
)

s3_resource = boto3.resource("s3")
s3_bucket = s3_resource.Bucket(os.environ["CONNECTION_STORE_BUCKET_NAME"])
s3_prefix = os.environ["CONNECTION_STORE_PREFIX"]


def input_controller(event, context):
    """
    Handle input from our input SNS topic
    """
    print("Input Data Event!")
    print(json.dumps(event))

    message: Dict[str, Any] = json.loads(event["Records"][0]["Sns"]["Message"])
    print(f"Message to send: {json.dumps(message)}")

    # Get all of our open connections
    s3_client = s3_resource.meta.client
    paginator = s3_client.get_paginator("list_objects_v2")
    for response in paginator.paginate(Bucket=s3_bucket.name, Prefix=s3_prefix):
        for s3_object_data in response.get("Contents", []):
            connection_id = s3_object_data["Key"][len(s3_prefix) + 1 :]
            print(f"Sending to {connection_id}")
            api_gateway_management_api_client.post_to_connection(
                ConnectionId=connection_id,
                Data=json.dumps(message).encode("utf-8"),
            )


def connect_controller(event, context):
    """
    Connection event - new websocket connection
    """
    print("Connect Event")
    print(json.dumps(event))
    s3_bucket.put_object(
        Key=f"{s3_prefix}/{event['requestContext']['connectionId']}", Body=b""
    )

    return {"statusCode": 200}


def disconnect_controller(event, context):
    """
    Disconnection event - closing an existing websocket connection
    """
    print("Disconnect Event")
    print(json.dumps(event))
    connection_key = f"{s3_prefix}/{event['requestContext']['connectionId']}"
    print(f"Removing {connection_key}...")
    try:
        result = s3_bucket.delete_objects(
            Delete={
                "Objects": [
                    {"Key": f"{s3_prefix}/{event['requestContext']['connectionId']}"}
                ]
            }
        )
        print(result)
    except Exception as err:
        print(err)

    return {"statusCode": 200}


def handler(event, context):
    if event.get("Records", None) is not None:
        return input_controller(event, context)
    if event.get("requestContext", {}).get("eventType", "") == "CONNECT":
        return connect_controller(event, context)
    elif event.get("requestContext", {}).get("eventType", "") == "DISCONNECT":
        return disconnect_controller(event, context)

    print("Got Unknown Event!")
    print(json.dumps(event))
    return {"statusCode": 500}
