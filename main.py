import boto3
from multiprocessing import Lock, JoinableQueue
from worker import Worker

workers_number = 4


def fill_queue(queue):
    s3 = boto3.resource("s3")
    for bucket in s3.buckets.all():
        queue.put((bucket.name, bucket.creation_date))

    for i in range(0, workers_number):
        queue.put(None)


def main():
    queue = JoinableQueue()
    workers = []

    fill_queue(queue)

    for i in range(0, workers_number):
        p = Worker(queue)
        workers.append(p)
        p.start()

    queue.join()

    for worker in workers:
        worker.join()


if __name__ == "__main__":
    main()
