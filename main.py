import boto3
from multiprocessing import Lock, Queue
from worker import Worker

workers_number = 5


def fill_queue(queue):
    s3 = boto3.resource("s3")
    for bucket in s3.buckets.all():
        queue.put(bucket.name)


def main():
    queue = Queue()
    lock = Lock()
    workers = []

    fill_queue(queue)

    for i in range(0, workers_number):
        p = Worker(queue, lock)
        workers.append(p)
        p.start()

    for worker in workers:
        worker.join()


if __name__ == "__main__":
    main()
