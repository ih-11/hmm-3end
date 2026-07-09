#!/usr/bin/env python3

import argparse
import re
import sys
import korflab

parser = argparse.ArgumentParser(
	description='extract fixed-length 3end candidate sequences')
parser.add_argument('fastq', help='input fastq file')
parser.add_argument('--min-len', type=int, default=15,
	help='minimum A/T run length')
parser.add_argument('--seq-len', type=int, default=100,
	help='sequence length before tail')
parser.add_argument('--tail-len', type=int, default=20,
	help='tail length in output')
parser.add_argument('--report', type=int, default=0,
	help='report progress every N reads')
arg = parser.parse_args()

apat = re.compile('A' * arg.min_len + '+')
tpat = re.compile('T' * arg.min_len + '+')

total = 0
out = 0
ahit = 0
thit = 0
edge = 0

for name, seq, plus, qual in korflab.readfastq(arg.fastq):
	total += 1

	if arg.report > 0 and total % arg.report == 0:
		print(f'[progress] processed {total} reads', file=sys.stderr)

	am = apat.search(seq)
	tm = tpat.search(seq)

	if am:
		beg = am.start() - arg.seq_len
		end = am.start() + arg.tail_len

		if beg < 0 or end > len(seq):
			edge += 1
			continue

		outseq = seq[beg:end]
		run = len(am.group())
		ahit += 1

	elif tm:
		beg = tm.end() - arg.tail_len
		end = tm.end() + arg.seq_len

		if beg < 0 or end > len(seq):
			edge += 1
			continue

		outseq = korflab.anti(seq[beg:end])
		run = len(tm.group())
		thit += 1

	else:
		continue

	read_id = name.split()[0]
	print(f'>{read_id} run={run} len={len(outseq)}')
	print(outseq)
	out += 1

print('[summary]', file=sys.stderr)
print('input_reads', total, sep='\t', file=sys.stderr)
print('output_reads', out, sep='\t', file=sys.stderr)
print('polyA_reads', ahit, sep='\t', file=sys.stderr)
print('polyT_reads', thit, sep='\t', file=sys.stderr)
print('edge_skipped', edge, sep='\t', file=sys.stderr)