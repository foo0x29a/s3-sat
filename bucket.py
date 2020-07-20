class Bucket():
    def __init__(self, s3, name):
        self.__bucket = s3.Bucket(name)
        self.__name = self.__bucket.name
        self.__creation_date = self.__bucket.creation_date
        self.__number_of_files = self.__count_files()

    def __count_files(self):
        return sum(1 for _ in self.__bucket.objects.all())

    def __str__(self):
        return (
            f"Bucket Name: {self.__name}\n"
            f"Creation Date: {self.__creation_date}\n"
            f"Number of Files: {self.__number_of_files}\n"
        )
