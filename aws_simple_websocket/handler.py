import os
from typing import Optional

import boto3


from aws_simple_websocket.connection_repo.s3 import S3ConnectionRepo
from aws_simple_websocket.websocket_router import WebsocketRouter

# "Cache" our router so we can re-use initialized AWS services, as is best practice
websocket_router: Optional[WebsocketRouter] = None


def handler(event, context):
    """
    Lambda entry point. Initializes our "router" which just has a some properties on it used to communicate with other
    AWS services and a route() method we can use to process messages
    """
    global websocket_router
    if websocket_router is None:
        # Create connections once in Lambda. Once our function "freezes", it can "thaw" without having to reconnect,
        # sometimes.

        # Setup management client specific to our API Gateway
        # https://github.com/boto/botocore/issues/2218
        api_gateway_management_api_client = boto3.client(
            "apigatewaymanagementapi", endpoint_url=os.environ["EXECUTE_API_ENDPOINT"]
        )

        # Instantiate a Connection Repository, that we made, of our choosing. We are using S3 to store connection
        # information, so create one of those objects with our config. This could be further extended to use DynamoDB,
        # Redis, or any other listable Key/Value store. S3 was just the simplest.
        websocket_connection_repo = S3ConnectionRepo(
            bucket_name=os.environ["CONNECTION_STORE_BUCKET_NAME"],
            prefix=os.environ["CONNECTION_STORE_PREFIX"],
        )
        websocket_router = WebsocketRouter(
            api_gateway_management_api_client=api_gateway_management_api_client,
            websocket_connection_repo=websocket_connection_repo,
        )

    return websocket_router.route(event, context)
