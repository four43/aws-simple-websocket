from collections import namedtuple
from dataclasses import dataclass, field
from typing import List, Any, Optional


@dataclass
class MockS3ObjectSummary:
    key: str


@dataclass
class MockS3Bucket:
    name: str = ""
    called_ops: List[Any] = field(default_factory=list)

    object_keys: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.objects = MockS3BucketObjects(self)

    def put_object(self, **kwargs):
        self.object_keys.append(kwargs["Key"])
        self.called_ops.append({"method": "put_object", "args": kwargs})

    def delete_objects(self, **kwargs):
        try:
            [self.object_keys.remove(x["Key"]) for x in kwargs["Delete"]["Objects"]]
        except ValueError:
            pass
        self.called_ops.append({"method": "delete_objects", "args": kwargs})


@dataclass
class MockS3BucketObjects:
    bucket: MockS3Bucket

    called_ops: List[Any] = field(default_factory=list)

    def filter(self, **kwargs):
        self.called_ops.append({"method": "filter", "args": kwargs})
        for key in self.bucket.object_keys:
            yield MockS3ObjectSummary(key=key)


class MockS3Resource:
    bucket: Optional[MockS3Bucket] = None

    def Bucket(self, bucket_name: str):
        self.bucket = MockS3Bucket(name=bucket_name)
        return self.bucket
