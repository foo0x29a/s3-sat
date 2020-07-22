import aioboto3
import re


class Bucket:
    def __init__(self, name, creation_date, key_filter):
        self.__name = name
        self.__creation_date = creation_date
        self.__key_filter = key_filter

    async def process_bucket(self):
        async with aioboto3.resource("s3") as s3:
            bucket = await s3.Bucket(self.__name)
            (
                self.__number_of_files,
                self.__size,
                self.__most_recent_file,
                self.__last_modified,
            ) = await self.__process_files(bucket)
            print(self)

    async def __process_files(self, bucket):
        number_of_files = 0
        total_size = 0.0
        most_recent_file = ""
        last_modified = ""

        async for object in bucket.objects.all():
            match = re.match(self.__key_filter, object.key)
            if not match:
                continue
            size = await object.size
            date = await object.last_modified
            if last_modified == "" or date > last_modified:
                last_modified = date
                most_recent_file = object.key
            if size > 0:
                number_of_files += 1
            total_size += size

        return number_of_files, total_size, most_recent_file, last_modified

    def __format_bytes(self, size):
        power = 2 ** 10
        n = 0
        power_labels = {0: "", 1: "K", 2: "M", 3: "G", 4: "T"}
        while size > power:
            size /= power
            n += 1
        return f"{size} {power_labels[n]}B"

    def __calculate_cost(self, size):
        gb = size/1024/1024/1024
        # rough cost estimate based on the us-east-1 price
        price = gb * 0.023
        return f'{price:.3f}'

    def __str__(self):
        return (
            f"Bucket Name: {self.__name}\n"
            f"Creation Date: {self.__creation_date}\n"
            f"Number of Files: {self.__number_of_files}\n"
            f"Total Size: {self.__format_bytes(self.__size)}\n"
            f"Total Cost: USD {self.__calculate_cost(self.__size)}\n"
            f"Most Recent Updated File: {self.__most_recent_file} Last Modified: {self.__last_modified}\n"
        )
