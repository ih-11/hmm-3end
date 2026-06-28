#!/usr/bin/env python3

import argparse
import gzip
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("fasta", help="Input mRNA FASTA file, can be .fa or .fa.gz")
args = parser.parse_args()

if args.fasta.endswith(".gz"):
    open_func = gzip.open
else:
    open_func = open

lengths = []
current_seq = []

with open_func(args.fasta, "rt") as f:
    for line in f:
        line = line.strip()

        if line.startswith(">"):
            if current_seq:
                lengths.append(len("".join(current_seq)))
            current_seq = []
        else:
            current_seq.append(line)

if current_seq:
    lengths.append(len("".join(current_seq)))

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

print(f"n_mRNAs\t{len(lengths)}")
print(f"predicted_mean_length\t{s.mean():.3f}")
print(f"predicted_stdev_length\t{s.std():.3f}")
print(f"predicted_median_length\t{s.median():.3f}")
print(f"predicted_n50\t{n50}")
print(f"predicted_min_length\t{s.min()}")
print(f"predicted_max_length\t{s.max()}")
