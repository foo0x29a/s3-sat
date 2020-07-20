from multiprocessing import Process
from bucket import Bucket


class Worker(Process):
    def __init__(self, queue, lock):
        self.__queue = queue
        self.__lock = lock
        super().__init__()

    def run(self):
        while not self.__queue.empty():
            bucket_name = self.__queue.get()
            bucket = Bucket(bucket_name)
            self.__lock.acquire()
            print(bucket)
            self.__lock.release()
