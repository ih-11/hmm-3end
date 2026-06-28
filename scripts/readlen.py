#!/usr/bin/env python3

import argparse
import gzip
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("fastq", help="Input FASTQ.gz file")
args = parser.parse_args()

lengths = []

with gzip.open(args.fastq, "rt") as f:
    while True:
        header = f.readline().strip()
        seq = f.readline().strip()
        plus = f.readline().strip()
        qual = f.readline().strip()

        if not header:
            break

        lengths.append(len(seq))

lengths_sorted = sorted(lengths, reverse=True)
total_bases = sum(lengths_sorted)
half_total_bases = total_bases / 2

running_total = 0
n50 = None

for length in lengths_sorted:
    running_total += length
    if running_total >= half_total_bases:
        n50 = length
        break

s = pd.Series(lengths)

print(f"n_reads\t{len(lengths)}")
print(f"mean_length\t{s.mean():.3f}")
print(f"stdev_length\t{s.std():.3f}")
print(f"median_length\t{s.median():.3f}")
print(f"n50\t{n50}")
print(f"min_length\t{s.min()}")
print(f"max_length\t{s.max()}")
