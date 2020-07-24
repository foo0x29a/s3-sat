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
    parser.add_argument(
        "--acl",
        action='store_true',
        help="Include Acl subresource",
    )
    parser.add_argument(
        "--cors",
        action='store_true',
        help="Include CORS subresource",
    )
    parser.add_argument(
        "--lifecycle",
        action='store_true',
        help="Include Lifecycle subresource",
    )
    parser.add_argument(
        "--logging",
        action='store_true',
        help="Include Logging subresource",
    )
    parser.add_argument(
        "--policy",
        action='store_true',
        help="Include Policy subresource",
    )
    parser.add_argument(
        "--tagging",
        action='store_true',
        help="Include Tagging subresource",
    )
    args = parser.parse_args()

    filters = {"bucket_filter": args.bucket_filter, "key_filter": args.key_filter}
    subresources = {"acl":args.acl, "cors":args.cors, "lifecycle":args.lifecycle, "logging":args.logging, "policy":args.policy, "tagging":args.tagging}
    start_workers(args.workers, filters, subresources)


if __name__ == "__main__":
    main()
