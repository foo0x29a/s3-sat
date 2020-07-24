# S3 Storage Analysis Tool

This project is intended to work as a shell like tool to perform basic operations against a given S3 repository.
It outputs something like this:
```
$ python main.py --bucket-filter='bucket.*' --key-filter='object.*'

Bucket Name: bucket01
Creation Date: 2020-07-21 02:15:11+00:00
Number of Files: 3
Total Size: 6.7900390625 KB
Total Cost: USD 0.000
Most Recent Updated File: object.json Last Modified: 2020-07-21 02:17:40+00:00

Bucket Name: bucket02
Creation Date: 2020-07-19 19:03:12+00:00
Number of Files: 0
Total Size: 0.0 B
Total Cost: USD 0.000
Most Recent Updated File:  Last Modified:
```

# Requirements
- Python >= 3.8 or Docker
- AWS credentials set either with environment variables or at `~/.aws/credentials`

# Usage
```
$ python main.py -h
usage: main.py [-h] [--workers WORKERS] [--bucket-filter BUCKET_FILTER] [--key-filter KEY_FILTER] [--acl] [--cors] [--lifecycle]
               [--logging] [--policy] [--tagging]

optional arguments:
  -h, --help            show this help message and exit
  --workers WORKERS, -w WORKERS
                        Number of workers. A good heuristic is: max((number_of_cpus - 1), 1)
  --bucket-filter BUCKET_FILTER, -b BUCKET_FILTER
                        Regular expression to filter buckets
  --key-filter KEY_FILTER, -k KEY_FILTER
                        Regular expression to filter keys
  --acl                 Include Acl subresource
  --cors                Include CORS subresource
  --lifecycle           Include Lifecycle subresource
  --logging             Include Logging subresource
  --policy              Include Policy subresource
  --tagging             Include Tagging subresource

```

# Standalone
## Installation
```
$ python -m pip install -r requirements.txt
```
## Running
```
$ python main.py
```

# As a Package
## Build
```
$ python setup.py sdist bdist_wheel
```
## Installation
```
# VERSION should be replaced by the current version in the setup.py
$ python -m pip install -r requirements.txt
$ python -m pip install ./dist/s3-sat-${VERSION}.tar.gz
```
## Running
```
$ python -m s3_sat
```

# Docker
## Build
```
$ docker build -t s3_sat .
```
## Running
```
# either sharing the credentials file
$ docker run -v /home/rdash/.aws/credentials:/root/.aws/credentials --rm -it s3_sat

# or setting the AWS environment variables
docker run -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} --rm -it s3_sat
```

## Design
```
                    .-------------.
              .-----| Main Thread |------.
             /      '-------------'       \
            /              .               \
           /               |                \
          /                |                 \
         '                 '                  '
   .----------.      .----------.       .----------.
   | Worker-1 |      | Worker-2 |       | Worker-N |
   '----------'      '----------'       '----------'
        ^                  ^                  ^
        |                  |                  |
        |                  |                  |
        |                  |                  |
        |                  |                  |
        |  AsyncIO         |  AsyncIO         | AsyncIO
        |                  |                  |
        |                  |                  |
        |                  v                  |
        |              _.-----._              |
        |            .-         -.            |
        |            |-_       _-|            |
        ---------->  |  ~-----~  | <-----------
                     |    s3     |
                     `._       _.'
                        "-----"   
```

- The multiprocess behavior was included to take advantage of multi cores
- AsyncIO can maximize the usage of each worker's thread while donwloading content from S3

# Caveats
- It lacks a good way of calculating the total cost of a bucket. It uses a rough cost estimate based on the us-east-1 region.
- Currently, the subresources (e.g.: CORS, tagging etc) are being fetched synchronously, which adds an overhead proportional to the number of buckets.
- It's not easy to test asyncIO operations of boto3
