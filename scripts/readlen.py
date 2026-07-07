#!/usr/bin/env python3

import argparse
import statistics
import korflab

parser = argparse.ArgumentParser(
	description='report length stats for fastq reads')
parser.add_argument('fastq', help='input fastq file')
arg = parser.parse_args()

lens = []

for header, seq, plus, qual in korflab.readfastq(arg.fastq):
	lens.append(len(seq))

lens_sorted = sorted(lens, reverse=True)
half = sum(lens_sorted) / 2

total = 0
n50 = None

for length in lens_sorted:
	total += length
	if total >= half:
		n50 = length
		break

print('n_reads', len(lens), sep='\t')
print('mean_length', f'{statistics.mean(lens):.3f}', sep='\t')
print('stdev_length', f'{statistics.stdev(lens):.3f}', sep='\t')
print('median_length', f'{statistics.median(lens):.3f}', sep='\t')
print('n50', n50, sep='\t')
print('min_length', min(lens), sep='\t')
print('max_length', max(lens), sep='\t')