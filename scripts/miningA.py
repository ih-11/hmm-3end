#!/usr/bin/env python3

import argparse
import gzip
import re

parse = argparse.ArgumentParser()
parse.add_argument("fastq", help = "Input FASTQ.gz")
parse.add_argument("--min-a", type=int, default=15, help="Min Poly-A length")
parse.add_argument("--up", type=int, default=100, help="Upstream Seq. of Poly-A")
arg = parse.parse_args()

pattern = re.compile("A", arg.min_a + "+")

with gzip.open(arg.fastq, "rt") as f:
    while True:
        header = f.readline().strip()
        seq = f.readline().strip()
        plus = f.readline()
        qual = f.readline()

        if not header:
            break

        match = pattern.search(seq)

        if match:
            start = match.start() - arg.up
            if start < 0:
                start = 0

            outseq = seq[start:]
            print(outseq)