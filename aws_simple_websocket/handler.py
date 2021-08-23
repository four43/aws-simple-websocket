import json
import os
from typing import Dict, Any

import boto3

# Setup management client specific to our API Gateway
# https://github.com/boto/botocore/issues/2218
from aws_simple_websocket.connection_repo.s3 import S3ConnectionRepo

api_gateway_management_api_client = boto3.client(
    "apigatewaymanagementapi", endpoint_url=os.environ["EXECUTE_API_ENDPOINT"]
)

# Instantiate a Connection Repository, that we made, of our choosing. We are using S3 to store connection information,
# so create one of those objects with our config. This could be further extended to use DynamoDB, Redis, or any other
# listable Key/Value store. S3 was just the simplest.
websocket_connection_repo = S3ConnectionRepo(
    bucket_name=os.environ["CONNECTION_STORE_BUCKET_NAME"],
    prefix=os.environ["CONNECTION_STORE_PREFIX"],
)


def sns_input_controller(event, context):
    """
    Handle input from our input SNS topic, broadcast to all clients
    """
    print("Input Data Event!")
    print(json.dumps(event))

    message: Dict[str, Any] = json.loads(event["Records"][0]["Sns"]["Message"])
    print(f"Message to send: {json.dumps(message)}")

    # Send this message to all of our open clients
    for connection_id in websocket_connection_repo.list_all():
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
    websocket_connection_repo.save(connection_id=event['requestContext']['connectionId'])
    return {"statusCode": 200}


def disconnect_controller(event, context):
    """
    Disconnection event - closing an existing websocket connection
    """
    print("Disconnect Event")
    print(json.dumps(event))
    connection_id = event['requestContext']['connectionId']
    print(f"Removing {connection_id}...")
    websocket_connection_repo.delete(connection_id=connection_id)

    return {"statusCode": 200}


def handler(event, context):
    if event.get("Records", None) is not None:
        # Received SNS event
        return sns_input_controller(event, context)
    if event.get("requestContext", {}).get("eventType", "") == "CONNECT":
        return connect_controller(event, context)
    elif event.get("requestContext", {}).get("eventType", "") == "DISCONNECT":
        return disconnect_controller(event, context)

    print("Got Unknown Event!")
    print(json.dumps(event))
    return {"statusCode": 500}
