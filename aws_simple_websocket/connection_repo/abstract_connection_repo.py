from abc import ABCMeta, abstractmethod
from typing import Iterator


class AbstractConnectionRepo(metaclass=ABCMeta):
    """
    Persist connection IDs from the API Gateway so we can retrieve them and know who to send messages to.
    """

    @abstractmethod
    def delete(self, connection_id: str):
        """
        Removes a `connection_id` from the store. Don't throw, this should act as desired state. If it's already
        gone, fair enough.
        """
        pass

    @abstractmethod
    def list_all(self) -> Iterator[str]:
        """
        Returns all of the connections. These should all be active but not guaranteed.
        """

    @abstractmethod
    def save(self, connection_id: str):
        """
        Saves a `connection_id` to the store
        """
        pass
