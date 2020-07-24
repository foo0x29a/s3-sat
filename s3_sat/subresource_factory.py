import importlib

class SubResourceFactory():
    subresource_map = {"acl":"BucketAcl", "cors":"BucketCors", "lifecycle":"BucketLifecycle", "logging":"BucketLogging", "policy":"BucketPolicy", "tagging":"BucketTagging"}

    @classmethod
    def create(cls, bucket, subresources):
        subresource_list = []
        module = importlib.import_module("s3_sat.bucket_subresource")
        for subresource_name, should_create in subresources.items():
            if should_create:
                subresource = getattr(module, cls.subresource_map[subresource_name])
                subresource_list.append({subresource_name:subresource(bucket).get_content()})

        return subresource_list
