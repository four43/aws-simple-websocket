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


@pytest.fixture
def api_gateway_management_api_client():
    return boto3.client(
        "apigatewaymanagementapi", endpoint_url=os.environ["TEST_EXECUTE_API_ENDPOINT"]
    )
