import pytest

from aws_simple_websocket.connection_repo.s3 import S3ConnectionRepo
from tests.unit.connection_repo import MockS3Resource


@pytest.fixture
def s3_resource():
    return MockS3Resource()


@pytest.fixture
def s3_repo(s3_resource):
    return S3ConnectionRepo(
        bucket_name="test-bucket", prefix="my-test-prefix", s3_resource=s3_resource
    )


def test_save_connection_id(s3_repo):
    s3_repo.save("abc123")
    assert s3_repo.bucket.called_ops == [
        {
            "method": "put_object",
            "args": {"Body": b"", "Key": "my-test-prefix/abc123"},
        }
    ]


def test_delete_connection_id(s3_repo):
    s3_repo.delete("abc123")
    assert s3_repo.bucket.called_ops == [
        {
            "method": "delete_objects",
            "args": {"Delete": {"Objects": [{"Key": "abc123"}]}},
        }
    ]


def test_list_all_connection_ids(s3_repo):
    s3_repo.save("abc123")
    s3_repo.save("def456")
    entries = list(s3_repo.list_all())
    assert entries == ["abc123", "def456"]
