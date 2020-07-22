import asyncio
from multiprocessing import Process
from .bucket import Bucket


class Worker(Process):
    def __init__(self, queue):
        self.__queue = queue
        super().__init__()

    def run(self):
        asyncio.run(self.__process_buckets())

    async def __process_buckets(self):
        aio_tasks = []

        while True:
            bucket_info = self.__queue.get()
            # sentinel
            if bucket_info == None:
                break
            bucket = Bucket(bucket_info[0], bucket_info[1])
            aio_task = asyncio.create_task(bucket.process_bucket())
            aio_tasks.append(aio_task)
            self.__queue.task_done()

        self.__queue.task_done()

        for aio_task in aio_tasks:
            await aio_task
