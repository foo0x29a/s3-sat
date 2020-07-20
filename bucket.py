class Bucket:
    def __init__(self, s3, name):
        self.__bucket = s3.Bucket(name)
        self.__name = self.__bucket.name
        self.__creation_date = self.__bucket.creation_date
        (
            self.__number_of_files,
            self.__size,
            self.__most_recent_file,
            self.__last_modified,
        ) = self.__process_files()

    def __process_files(self):
        number_of_files = 0
        total_size = 0.0
        most_recent_file = ""
        last_modified = ""

        for object in self.__bucket.objects.all():
            size = object.size
            date = object.last_modified
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

    def __str__(self):
        return (
            f"Bucket Name: {self.__name}\n"
            f"Creation Date: {self.__creation_date}\n"
            f"Number of Files: {self.__number_of_files}\n"
            f"Total Size: {self.__format_bytes(self.__size)}\n"
            f"Most Recent Updated File: {self.__most_recent_file} Last Modified: {self.__last_modified}\n"
        )
