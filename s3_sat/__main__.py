import argparse
from .run import start_workers


def workers_type(n):
    n = int(n)
    if n <= 0:
        raise argparse.ArgumentTypeError("Minimum workers is 1")
    return n


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--workers",
        "-w",
        type=workers_type,
        help="Number of workers. A good heuristic is: max((number_of_cpus - 1), 1)",
        default=1,
    )
    parser.add_argument(
        "--bucket-filter",
        "-b",
        type=str,
        help="Regular expression to filter buckets",
        default=".*",
    )
    parser.add_argument(
        "--key-filter",
        "-k",
        type=str,
        help="Regular expression to filter keys",
        default=".*",
    )
    args = parser.parse_args()

    start_workers(args.workers, args.bucket_filter, args.key_filter)


if __name__ == "__main__":
    main()
