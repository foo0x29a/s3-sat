from moto import mock_s3
from s3_sat import run
from multiprocessing import JoinableQueue

@mock_s3
def test_get_buckets(s3):
    s3.create_bucket(Bucket="testing")
    buckets = run.get_buckets()

    assert len(buckets) == 1

def test_add_sentinels():
    queue = JoinableQueue()
    run.add_sentinels(queue, 2)

    queue.get()

    assert queue.get() == None

@mock_s3
def test_fill_queue(s3):
    queue = JoinableQueue()
    s3.create_bucket(Bucket="testing")
    s3.create_bucket(Bucket="gnitset")
    buckets = run.get_buckets()

    run.fill_queue(queue, buckets, "test.*")

    assert queue.get() is not None
