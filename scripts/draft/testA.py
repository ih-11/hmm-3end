#!/usr/bin/env python3

import argparse
import re
import korflab

parser = argparse.ArgumentParser(
	description='inspect sequence around poly-A or poly-T runs')
parser.add_argument('fastq', help='input fastq file')
parser.add_argument('--min-len', type=int, default=15,
	help='minimum A/T run length')
parser.add_argument('--seq-len', type=int, default=100,
	help='transcript-side sequence length')
arg = parser.parse_args()

apat = re.compile('A' * arg.min_len + '+')
tpat = re.compile('T' * arg.min_len + '+')

for header, seq, plus, qual in korflab.readfastq(arg.fastq):
	read_id = header.split()[0]

	am = apat.search(seq)
	tm = tpat.search(seq)

	if am:
		beg = am.start() - arg.seq_len

		if beg < 0:
			continue

		outseq = seq[beg:]
		run = len(am.group())

		print(
			f'>{read_id} source=A '
			f'lenA={run} len_read={len(seq)}')
		print(outseq)

	elif tm:
		end = tm.end() + arg.seq_len

		if end > len(seq):
			continue

		outseq = korflab.anti(seq[:end])
		run = len(tm.group())

		print(
			f'>{read_id} source=T_rc '
			f'lenA={run} len_read={len(seq)}')
		print(outseq)