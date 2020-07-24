import boto3
from abc import abstractmethod, ABCMeta
from botocore import exceptions

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

class BucketCors(BucketSubResource):
    def __init__(self, bucket):
        super().__init__(bucket)

    def get_content(self):
        try:
            cors = [self._bucket.Cors().cors_rules]
        except exceptions.ClientError:
            print("No CORS configuration")
            cors = ["No CORS configuration"]
        return cors

class BucketLifecycle(BucketSubResource):
    def __init__(self, bucket):
        super().__init__(bucket)

    def get_content(self):
        try:
            lifecycle = [self._bucket.Lifecycle().rules]
        except exceptions.ClientError:
            print("No lifecycle configuration")
            lifecycle = ["No lifecycle configuration"]

        return lifecycle

class BucketLogging(BucketSubResource):
    def __init__(self, bucket):
        super().__init__(bucket)

    def get_content(self):
        logging_enabled = [self._bucket.Logging().logging_enabled]
        if not logging_enabled:
            logging_enabled = False
        return logging_enabled
