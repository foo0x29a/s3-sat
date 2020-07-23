from s3_sat.worker import Worker
from multiprocessing import JoinableQueue

def test_worker():
    queue = JoinableQueue()
    queue.put(None)
    key_filter = ".*"

    worker = Worker(queue, key_filter)
    worker.start()
    worker.join()

    queue.put(None)

    assert queue.get() == None
