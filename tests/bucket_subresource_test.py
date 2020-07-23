import pytest
from moto import mock_s3
from botocore import exceptions
from s3_sat.bucket_subresource import BucketAcl
from s3_sat.bucket_subresource import BucketCors


@mock_s3
def test_get_acl(s3):
    s3.create_bucket(Bucket="testing")
    bucket = s3.Bucket("testing")
    bucket_acl = BucketAcl(bucket)
    content = bucket_acl.get_content()

    assert len(content) == 2


@mock_s3
def test_get_cors_exception(s3):
    s3.create_bucket(Bucket="testing")
    bucket = s3.Bucket("testing")
    bucket_cors = BucketCors(bucket)

    content = bucket_cors.get_content()

    assert content.pop() == "No CORS configuration"


@mock_s3
def test_get_cors(s3, s3_client):
    s3.create_bucket(Bucket="testing")
    bucket = s3.Bucket("testing")
    cors_configuration = {
        "CORSRules": [
            {
                "AllowedHeaders": ["Authorization"],
                "AllowedMethods": ["GET", "PUT"],
                "AllowedOrigins": ["*"],
            }
        ]
    }
    s3_client.put_bucket_cors(Bucket="testing", CORSConfiguration=cors_configuration)

    bucket_cors = BucketCors(bucket)
    content = bucket_cors.get_content()

    assert len(content) == 1
