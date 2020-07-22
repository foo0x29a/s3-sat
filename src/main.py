import boto3
from multiprocessing import Lock, JoinableQueue
from .worker import Worker


def fill_queue(queue, workers_number):
    s3 = boto3.resource("s3")
    for bucket in s3.buckets.all():
        queue.put((bucket.name, bucket.creation_date))

    for i in range(0, workers_number):
        queue.put(None)


def start_workers(workers_number):
    queue = JoinableQueue()
    workers = []

    fill_queue(queue, workers_number)

    for i in range(0, workers_number):
        p = Worker(queue)
        workers.append(p)
        p.start()

    queue.join()

    for worker in workers:
        worker.join()
