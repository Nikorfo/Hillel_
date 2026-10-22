# import sys
# print( sys.argv )
import argparse

parser = argparse.ArgumentParser(description="Orders reports")

parser.add_argument("path", help="Path to the file to open")
parser.add_argument("--min-total", type=float, default=0.0, help="Skip smaller orders")
parser.add_argument("--status", choices=["new", "paid", "all"], default="all", help="Status of the order")
parser.add_argument("-v", "--verbose", action="count", default=0)
parser.add_argument("--dry-run", action="store_true")

args = parser.parse_args()
print(args)
print(args.path, args.min_total, args.verbose)
