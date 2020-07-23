import boto3
from abc import abstractmethod, ABCMeta

class BucketSubResource(metaclass=ABCMeta):
    def __init__(self, bucket):
        self._bucket = bucket

    @abstractmethod
    def get_content(self):
        pass

class BucketAcl(BucketSubResource):
    def __init__(self, bucket):
        super().__init__(bucket)

    def get_content(self):
       return [self._bucket.Acl().owner, self._bucket.Acl().grants]

