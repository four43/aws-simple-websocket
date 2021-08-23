import pytest

from tests.conftest import get_fixture_json
from tests.integration.test_utils import (
    s3_bucket,
    s3_repo,
    api_gateway_management_api_client,
)

from aws_simple_websocket.websocket_router import WebsocketRouter


@pytest.fixture
def websocket_router(api_gateway_management_api_client, s3_repo):
    return WebsocketRouter(
        api_gateway_management_api_client=api_gateway_management_api_client,
        websocket_connection_repo=s3_repo,
    )


def test_websocket_send_gone(websocket_router):
    connect_event = get_fixture_json("connect_1.json")
    websocket_router.route(connect_event, {})
    assert list(websocket_router.websocket_connection_repo.list_all()) == [
        "EhbxcdD1IAMCLvQ="
    ]

    sns_message_event = get_fixture_json("sns_message_1.json")
    websocket_router.route(sns_message_event, {})
    assert list(websocket_router.websocket_connection_repo.list_all()) == []
