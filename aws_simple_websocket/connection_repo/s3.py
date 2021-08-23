from typing import Any, Iterator

import boto3

from aws_simple_websocket.connection_repo.abstract_connection_repo import (
    AbstractConnectionRepo,
)


class S3ConnectionRepo(AbstractConnectionRepo):
    """
    Persist connection IDs from the API Gateway so we can retrieve them and know who to send messages to by saving
    Connection IDs as S3 objects and later listing the S3 objects to get a list of active connections.
    """

    bucket: Any  # Bad type, but boto3 isn't made well
    prefix: str = ""

    def __init__(self, bucket_name: str, prefix: str, s3_resource: Any = None):
        super().__init__()
        # Inject in an S3 Resource so we can mock this easier in tests
        if s3_resource is None:
            s3_resource = boto3.resource("s3")

        self.bucket = s3_resource.Bucket(bucket_name)
        self.prefix = prefix

    def delete(self, connection_id: str):
        """
        Removes a `connection_id` from the store by deleting the S3 Object with that key. Don't throw, this should act
        as desired state. If it's already gone, fair enough.
        """
        self.bucket.delete_objects(Delete={"Objects": [{"Key": connection_id}]})

    def list_all(self) -> Iterator[str]:
        """
        Returns all of the connections by listing all of the objects in this store. These should all be active but not
        guaranteed.
        """
        for s3_obj_summary in self.bucket.objects.filter(Prefix=self.prefix):
            yield s3_obj_summary.key[len(self.prefix) + 1 :]

    def save(self, connection_id: str):
        """
        Saves a `connection_id` to S3 by creating an empty object with that ID as the key
        """
        self.bucket.put_object(Key=f"{self.prefix}/{connection_id}", Body=b"")
