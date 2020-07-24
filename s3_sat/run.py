import boto3
import re
from botocore import exceptions
from multiprocessing import Lock, JoinableQueue
from .worker import Worker

def get_buckets():
    s3 = boto3.resource("s3")

    try:
        buckets = list(s3.buckets.all())
    except exceptions.NoCredentialsError:
        print(
            "Auth Error: Please, either set necessary environment variables, or create the credentials config at ~/.aws"
        )
        exit(1)
    except exceptions.ClientError:
        print("Auth Error: Please, double check your credentials")
        exit(1)

    return buckets


def fill_queue(queue, buckets, bucket_filter):

    for bucket in buckets:
        match = re.match(bucket_filter, bucket.name)
        if match:
            queue.put((bucket.name, bucket.creation_date))


def add_sentinels(queue, workers_number):
    for i in range(0, workers_number):
        queue.put(None)


def start_workers(workers_number, filters):
    queue = JoinableQueue()
    workers = []

    buckets = get_buckets()
    fill_queue(queue, buckets, filters['bucket_filter'])
    add_sentinels(queue, workers_number)

    for i in range(0, workers_number):
        p = Worker(queue, filters['key_filter'])
        workers.append(p)
        p.start()

    queue.join()

    for worker in workers:
        worker.join()
