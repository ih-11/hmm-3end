#!/usr/bin/env python3

import argparse
import re
import korflab

parser = argparse.ArgumentParser(
	description='extract sequence around poly-A or poly-T runs')
parser.add_argument('fastq', help='input fastq file')
parser.add_argument('--min-len', type=int, default=15,
	help='minimum A/T run length')
parser.add_argument('--up', type=int, default=100,
	help='long side length')
parser.add_argument('--down', type=int, default=20,
	help='short side length')
parser.add_argument('--tail', choices=['A', 'T'], required=True,
	help='tail type')
arg = parser.parse_args()

pattern = re.compile(arg.tail * arg.min_len + '+')

for header, seq, plus, qual in korflab.readfastq(arg.fastq):
	read_id = header.split()[0]
	match = pattern.search(seq)

	if match:
		if arg.tail == 'A':
			beg = match.start() - arg.up
			end = match.end() + arg.down
		else:
			beg = match.start() - arg.down
			end = match.end() + arg.up

		if beg < 0: beg = 0
		if end > len(seq): end = len(seq)

		print(f'>{read_id}')
		print(seq[beg:end])