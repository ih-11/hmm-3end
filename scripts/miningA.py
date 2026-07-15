#!/usr/bin/env python3

import argparse
import re
import sys
import korflab

parser = argparse.ArgumentParser(
	description='extract sequence around poly-A or poly-T runs')
parser.add_argument('fastq', help='input fastq file')
parser.add_argument('--min-len', type=int, default=15,
	help='minimum A/T run length')
parser.add_argument('--seq-len', type=int, default=100,
	help='transcript-side sequence length')
parser.add_argument('--report', type=int, default=0,
	help='report progress every N reads')
arg = parser.parse_args()

apat = re.compile('A' * arg.min_len + '+')
tpat = re.compile('T' * arg.min_len + '+')

total = 0
output = 0
skipped = 0

for header, seq, plus, qual in korflab.readfastq(arg.fastq):
	total += 1

	if arg.report > 0 and total % arg.report == 0:
		print(f'processed {total} reads', file=sys.stderr)

	read_id = header.split()[0]

	am = apat.search(seq)
	tm = tpat.search(seq)

	if am:
		beg = am.start() - arg.seq_len
		end = am.end()
		run = len(am.group())

		if beg < 0:
			skipped += 1
			continue

		outseq = seq[beg:end]

	elif tm:
		beg = tm.start()
		end = tm.end() + arg.seq_len
		run = len(tm.group())

		if end > len(seq):
			skipped += 1
			continue

		outseq = korflab.anti(seq[beg:end])

	else:
		continue

	print(f'>{read_id} lenA={run} len_read={len(seq)}')
	print(outseq)
	output += 1

print('\nsummary', file=sys.stderr)
print('input_reads', total, sep='\t', file=sys.stderr)
print('output_reads', output, sep='\t', file=sys.stderr)
print('skipped_reads', skipped, sep='\t', file=sys.stderr)