import json
from dataclasses import dataclass
from typing import Any, Dict

import botocore

from aws_simple_websocket.connection_repo.abstract_connection_repo import (
    AbstractConnectionRepo,
)


@dataclass
class WebsocketRouter:
    """
    Bundle up some dependencies and routing logic into one object. Provides a main `route(event, context)` method that
    can be given various messages that our Lambda function may receive.
    """

    api_gateway_management_api_client: Any  # Bad typing because boto3 isn't made well
    websocket_connection_repo: AbstractConnectionRepo

    def route(self, event, context):
        if event.get("Records", None) is not None:
            # Received SNS event
            return self.sns_input_controller(event, context)
        if event.get("requestContext", {}).get("eventType", "") == "CONNECT":
            return self.connect_controller(event, context)
        elif event.get("requestContext", {}).get("eventType", "") == "DISCONNECT":
            return self.disconnect_controller(event, context)

        print("Got Unknown Event!")
        print(json.dumps(event))
        return {"statusCode": 500}

    def sns_input_controller(self, event, context):
        """
        Handle input from our input SNS topic, broadcast to all clients
        """
        print("Input Data Event!")
        print(json.dumps(event))

        message: Dict[str, Any] = json.loads(event["Records"][0]["Sns"]["Message"])
        print(f"Message to send: {json.dumps(message)}")

        # Send this message to all of our open clients
        for connection_id in self.websocket_connection_repo.list_all():
            print(f"Sending to {connection_id}")
            try:
                self.api_gateway_management_api_client.post_to_connection(
                    ConnectionId=connection_id,
                    Data=json.dumps(message).encode("utf-8"),
                )
            except self.api_gateway_management_api_client.exceptions.GoneException:
                self.websocket_connection_repo.delete(connection_id)

    def connect_controller(self, event, context):
        """
        Connection event - new websocket connection
        """
        print("Connect Event")
        print(json.dumps(event))
        self.websocket_connection_repo.save(
            connection_id=event["requestContext"]["connectionId"]
        )
        return {"statusCode": 200}

    def disconnect_controller(self, event, context):
        """
        Disconnection event - closing an existing websocket connection
        """
        print("Disconnect Event")
        print(json.dumps(event))
        connection_id = event["requestContext"]["connectionId"]
        print(f"Removing {connection_id}...")
        self.websocket_connection_repo.delete(connection_id=connection_id)

        return {"statusCode": 200}
