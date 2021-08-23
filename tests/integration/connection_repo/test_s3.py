import os

import boto3
import pytest

from aws_simple_websocket.connection_repo.s3 import S3ConnectionRepo


@pytest.fixture
def s3_bucket():
    s3_res = boto3.resource("s3")
    s3_bucket = s3_res.Bucket(os.environ["TEST_BUCKET_NAME"])
    s3_bucket.objects.delete()
    return s3_bucket


@pytest.fixture
def s3_repo(s3_bucket):
    return S3ConnectionRepo(bucket_name=s3_bucket.name, prefix="integration-tests")


def test_delete_save_connection(s3_bucket, s3_repo):
    s3_repo.save("abc123")
    assert list(s3_bucket.objects.all())[0].key == "integration-tests/abc123"


def test_delete_missing_connection_id(s3_repo):
    # Should succeed even though we've never created this
    s3_repo.delete("abc123")


def test_save_delete_multiple_connection(s3_bucket, s3_repo):
    s3_repo.save("abc123")
    s3_repo.delete("abc123")
    s3_repo.save("abc123")
    s3_repo.save("def456")
    assert list(s3_bucket.objects.all())[0].key == "integration-tests/abc123"
    assert list(s3_bucket.objects.all())[1].key == "integration-tests/def456"
