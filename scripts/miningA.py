#!/usr/bin/env python3

import argparse
import gzip
import re

parse = argparse.ArgumentParser()
parse.add_argument("fastq", help = "Input FASTQ.gz")
parse.add_argument("--min-a", type=int, default=15, help="Min Poly-A length")
parse.add_argument("--up", type=int, default=100, help="Upstream Seq. of Poly-A")
arg = parse.parse_args()