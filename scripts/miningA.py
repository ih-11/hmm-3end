#!/usr/bin/env python3

import argparse
import gzip
import re

parser = argparse.ArgumentParser()
parser.add_argument("fastq", help="Input FASTQ.gz")
parser.add_argument("--min-a", type=int, default=15, help="Minimum A/T run length")
parser.add_argument("--up", type=int, default=100, help="Upstream sequence length")
parser.add_argument("--tail", choices=["A", "T", "both"], default="A",
                    help="Tail type to search for")
args = parser.parse_args()

if args.tail == "A":
    patterns = [("A", re.compile("A" * args.min_a + "+"))]
elif args.tail == "T":
    patterns = [("T", re.compile("T" * args.min_a + "+"))]
else:
    patterns = [
        ("A", re.compile("A" * args.min_a + "+")),
        ("T", re.compile("T" * args.min_a + "+")),
    ]

with gzip.open(args.fastq, "rt") as f:
    while True:
        header = f.readline().strip()
        seq = f.readline().strip()
        plus = f.readline()
        qual = f.readline()

        if not header:
            break

        read_id = header.split()[0].replace("@", "")

        for tail_type, pattern in patterns:
            match = pattern.search(seq)

            if match:
                start = match.start() - args.up
                if start < 0:
                    start = 0

                outseq = seq[start:]

                print(f">{read_id}_{tail_type}")
                print(outseq)
                break