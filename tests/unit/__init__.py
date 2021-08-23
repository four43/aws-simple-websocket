from dataclasses import dataclass, field
from typing import List, Iterator, Dict, Any

from aws_simple_websocket.connection_repo.abstract_connection_repo import (
    AbstractConnectionRepo,
)


@dataclass
class MockWebsocketConnectionRepo(AbstractConnectionRepo):

    connection_ids: List[str] = field(default_factory=list)

    def list_all(self) -> Iterator[str]:
        return iter(self.connection_ids)

    def save(self, connection_id: str):
        self.connection_ids.append(connection_id)

    def delete(self, connection_id: str):
        try:
            self.connection_ids.remove(connection_id)
        except ValueError:
            pass


@dataclass
class MockAPIGatewayManagementApiClient:
    posted_messages: List[Dict[str, Any]] = field(default_factory=list)

    def post_to_connection(self, ConnectionId: str, Data: bytes):
        self.posted_messages.append({"ConnectionId": ConnectionId, "Data": Data})
