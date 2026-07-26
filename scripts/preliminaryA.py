#!/usr/bin/env python3

import argparse
import re
import korflab

parser = argparse.ArgumentParser(description='extract candidate 3end sequences')
parser.add_argument('fastq', help='input fastq file')
parser.add_argument('--min-len', type=int, default=15, help='minimum A/T run length')
parser.add_argument('--seq-len', type=int, default=100, help='transcript-side sequence length')
arg = parser.parse_args()

apat = re.compile('A' * arg.min_len + '+')
tpat = re.compile('T' * arg.min_len + '+')

for header, seq, plus, qual in korflab.readfastq(arg.fastq):
	read_id = header.split()[0]

	am = apat.search(seq)
	tm = tpat.search(seq)

	# The variable 'keep' is called a FLAG
	keep = None
	if am and tm: keep, status = False, 'both'
	elif am:      keep, status = True,  'polyA'
	elif tm:      keep, status = True,  'polyA'
	else:         keep, status = False, 'neither'

	if keep and am:
		beg = am.start() - arg.seq_len
		if beg < 0: keep, status = False, 'short'
		else:       outseq, run = seq[beg:am.end()], len(am.group())

	elif keep and tm:
		end = tm.end() + arg.seq_len
		if end > len(seq): keep, status = False, 'short'
		else:              outseq, run = korflab.anti(seq[tm.start():end]), len(tm.group())

	if keep:
		print(f'>{read_id} status=keep type={status} lenA={run} len_read={len(seq)}')
		print(outseq)
	else:
		print(f'>{read_id} status=reject reason={status} len_read={len(seq)}')
		print(seq)