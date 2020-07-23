import asyncio
import pytest
from datetime import date
from moto import mock_s3
from s3_sat.bucket import Bucket

def test_bucket():
    bucket = Bucket("testing", date.today(), ".*")
    assert bucket is not None
