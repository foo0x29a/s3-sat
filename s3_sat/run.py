import boto3
import re
from botocore import exceptions
from multiprocessing import Lock, JoinableQueue
from .worker import Worker


def fill_queue(queue, workers_number, bucket_filter):
    s3 = boto3.resource("s3")

    try:
        buckets = list(s3.buckets.all())
    except exceptions.NoCredentialsError:
        print("Auth Error: Please, either set necessary environment variables, or create the credentials config at ~/.aws")
        exit(1)

    for bucket in s3.buckets.all():
        match = re.match(bucket_filter, bucket.name)
        if match:
            queue.put((bucket.name, bucket.creation_date))

    for i in range(0, workers_number):
        queue.put(None)


def start_workers(workers_number, bucket_filter, key_filter):
    queue = JoinableQueue()
    workers = []

    fill_queue(queue, workers_number, bucket_filter)

    for i in range(0, workers_number):
        p = Worker(queue, key_filter)
        workers.append(p)
        p.start()

    queue.join()

    for worker in workers:
        worker.join()
