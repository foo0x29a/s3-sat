import pytest
from moto import mock_s3
from s3_sat.bucket_subresource import BucketAcl


@mock_s3
def test_get_acl(s3):
    s3.create_bucket(Bucket="testing")
    bucket = s3.Bucket("testing")
    bucket_acl = BucketAcl(bucket)
    content = bucket_acl.get_content()

    assert len(content) == 2
