import json
from pathlib import Path

import pytest

from aws_simple_websocket.websocket_router import WebsocketRouter
from tests.unit import MockWebsocketConnectionRepo, MockAPIGatewayManagementApiClient

FIXTURE_DIR = Path(__file__).parent.parent / "fixtures"


@pytest.fixture
def websocket_router():
    return WebsocketRouter(
        api_gateway_management_api_client=MockAPIGatewayManagementApiClient(),
        websocket_connection_repo=MockWebsocketConnectionRepo(),
    )


def get_fixture_json(fixture_name: str):
    with open(FIXTURE_DIR / fixture_name) as fixture_fh:
        return json.load(fixture_fh)


def test_connect(websocket_router):
    connect_event = get_fixture_json("connect_1.json")
    websocket_router.route(connect_event, {})
    assert len(websocket_router.websocket_connection_repo.connection_ids) == 1
    assert (
        websocket_router.websocket_connection_repo.connection_ids[0]
        == "EhbxcdD1IAMCLvQ="
    )


def test_connect_disconnect(websocket_router):
    connect_event = get_fixture_json("connect_1.json")
    websocket_router.route(connect_event, {})
    disconnect_event = get_fixture_json("disconnect_1.json")
    websocket_router.route(disconnect_event, {})
    assert len(websocket_router.websocket_connection_repo.connection_ids) == 0


def test_send_sns_message(websocket_router):
    connect_event = get_fixture_json("connect_1.json")
    websocket_router.route(connect_event, {})
    sns_message_event = get_fixture_json("sns_message_1.json")
    websocket_router.route(sns_message_event, {})
    assert len(websocket_router.api_gateway_management_api_client.posted_messages) == 1
    assert websocket_router.api_gateway_management_api_client.posted_messages[0] == {
        "ConnectionId": "EhbxcdD1IAMCLvQ=",
        "Data": b'{"hello": "world"}',
    }
