from tests.integration.test_utils import s3_bucket, s3_repo


def test_delete_save_connection(s3_bucket, s3_repo):
    s3_repo.save("abc123")
    assert list(s3_bucket.objects.all())[0].key == "integration-tests/abc123"


def test_delete_existing_connection(s3_bucket, s3_repo):
    s3_repo.save("abc123")
    assert list(s3_bucket.objects.all())[0].key == "integration-tests/abc123"
    s3_repo.delete("abc123")
    assert len(list(s3_bucket.objects.all())) == 0


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
