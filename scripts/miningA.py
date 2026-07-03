#!/usr/bin/env python3

import argparse
import gzip
import re

parser = argparse.ArgumentParser()
parser.add_argument("fastq", help="Input FASTQ.gz")
parser.add_argument("--min-len", type=int, default=15, help="Minimum A/T run length")
parser.add_argument("--up", type=int, default=100, help="Upstream sequence length")
parser.add_argument("--down", type=int, default=20, help="Downstream sequence lenght")
parser.add_argument("--tail", choices=["A", "T", "both"], default="A", help="Tail type A/T")

args = parser.parse_args()


if args.tail == "A":
    patterns = [("A", re.compile("A" * args.min_a + "+"))]
elif args.tail == "T":
    patterns = [("T", re.compile("T" * args.min_a + "+"))]
else:
    patterns = [
        ("A", re.compile("A" * args.min_a + "+")),
        ("T", re.compile("T" * args.min_a + "+"))
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
                if tail_type == "A":
                    start = match.start() - args.up
                    end = match.end() + args.down
                else:
                    start = match.start() - args.down
                    end = match.end() + args.up
                if start < 0:
                    start = 0
                if end > len(seq):
                    end = len(seq)
                outseq = seq[start:end]

                print(f">{read_id}_{tail_type}")
                print(outseq)

                break