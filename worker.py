import boto3
from multiprocessing import Process
from bucket import Bucket


class Worker(Process):
    def __init__(self, queue, lock):
        self.__s3 = boto3.resource("s3")
        self.__queue = queue
        self.__lock = lock
        super().__init__()

    def run(self):
        while not self.__queue.empty():
            bucket_name = self.__queue.get()
            bucket = Bucket(self.__s3, bucket_name)
            self.__lock.acquire()
            print(bucket)
            self.__lock.release()
