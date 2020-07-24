from datetime import datetime
import pytest
from moto import mock_s3
from botocore import exceptions
from s3_sat.bucket_subresource import BucketAcl
from s3_sat.bucket_subresource import BucketCors
from s3_sat.bucket_subresource import BucketLifecycle
from s3_sat.bucket_subresource import BucketLogging


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


@mock_s3
def test_get_lifecycle_exception(s3):
    s3.create_bucket(Bucket="testing")
    bucket = s3.Bucket("testing")
    bucket_lifecycle = BucketLifecycle(bucket)

    content = bucket_lifecycle.get_content()

    assert content.pop() == "No lifecycle configuration"


@mock_s3
def test_get_lifecycle(s3, s3_client):
    s3.create_bucket(Bucket="testing")
    bucket = s3.Bucket("testing")
    lifecycle = {
        "Rules": [
            {
                "Expiration": {"Days": 91,},
                "ID": "90-days-to-glacier",
                "Prefix": "",
                "Status": "Enabled",
                "Transitions": [{"Days": 90, "StorageClass": "GLACIER"},],
                "NoncurrentVersionTransitions": [
                    {"NoncurrentDays": 90, "StorageClass": "GLACIER"},
                ],
                "NoncurrentVersionExpiration": {"NoncurrentDays": 91},
            },
        ]
    }
    s3_client.put_bucket_lifecycle_configuration(
        Bucket="testing", LifecycleConfiguration=lifecycle
    )

    bucket_lifecycle = BucketLifecycle(bucket)
    content = bucket_lifecycle.get_content()

    assert len(content) == 1

@mock_s3
def test_get_logging(s3):
    s3.create_bucket(Bucket="testing")
    bucket = s3.Bucket("testing")
    bucket_logging = BucketLogging(bucket)
    content = bucket_logging.get_content()

    assert len(content) == 1
