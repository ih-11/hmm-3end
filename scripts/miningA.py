#!/usr/bin/env python3

import argparse
import re
import korflab

parser = argparse.ArgumentParser(
	description='extract fixed-length sequence around poly-A or poly-T runs')
parser.add_argument('fastq', help='input fastq file')
parser.add_argument('--min-len', type=int, default=15,
	help='minimum A/T run length')
parser.add_argument('--seq-len', type=int, default=100,
	help='transcript-side sequence length')
parser.add_argument('--tail-len', type=int, default=20,
	help='tail length in output')
arg = parser.parse_args()

apat = re.compile('A' * arg.min_len + '+')
tpat = re.compile('T' * arg.min_len + '+')

for header, seq, plus, qual in korflab.readfastq(arg.fastq):
	read_id = header.split()[0]

	am = apat.search(seq)
	tm = tpat.search(seq)

	if am:
		beg = am.start() - arg.seq_len
		end = am.start() + arg.tail_len

		if beg < 0 or end > len(seq): continue

		outseq = seq[beg:end]

	elif tm:
		beg = tm.end() - arg.tail_len
		end = tm.end() + arg.seq_len

		if beg < 0 or end > len(seq): continue

		outseq = korflab.anti(seq[beg:end])

	else:
		continue

	print(f'>{read_id}')
	print(outseq)