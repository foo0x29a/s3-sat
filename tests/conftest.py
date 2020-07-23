import boto3
import pytest
import os
from moto import mock_s3

@pytest.fixture(scope='function')
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'

@pytest.fixture(scope='function')
def s3(aws_credentials):
    with mock_s3():
        s3 = boto3.resource("s3")
        yield s3

@pytest.fixture(scope='function')
def s3_client(aws_credentials):
    with mock_s3():
        s3_client = boto3.client("s3")
        yield s3_client
