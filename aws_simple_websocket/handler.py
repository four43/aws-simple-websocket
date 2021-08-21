import json


def input_controller(event, context):
    """
    Handle input from our input SNS topic
    """
    print("Input Data Event!")
    print(event)


def connect_controller(event, context):
    """
    Connection event - new websocket connection
    """
    print("Connect Event")
    print(event)

    return {
        "statusCode": 200
    }


def disconnect_controller(event, context):
    """
    Disconnection event - closing an existing websocket connection
    """
    print("Disconnect Event")
    print(event)

    return {
        "statusCode": 200
    }


def handler(event, context):
    if event.get("Records", None) is not None:
        return input_controller(event, context)
    if event.get("requestContext", {}).get("eventType", "") == "CONNECT":
        return connect_controller(event, context)
    elif event.get("requestContext", {}).get("eventType", "") == "DISCONNECT":
        return disconnect_controller(event, context)

    print("Got Unknown Event!")
    print(json.dumps(event))
    return {
        "statusCode": 500
    }
