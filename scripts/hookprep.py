#!/usr/bin/env python3

import argparse
import korflab

parser = argparse.ArgumentParser(
	description='generate polyA/polyT hook sequences for blastA.py')
parser.add_argument('--min-len', type=int, default=15,
	help='length of A/T homopolymer run [%(default)i]')
parser.add_argument('--prefix', type=int, default=20,
	help='length of adapter prefix used in hook [%(default)i]')
parser.add_argument('--adapter',
	default='CTTGCGGGCGGCGGACTCTCCTCTGAAGATAGAGCGACAGGCAAG',
	help='CRTA sequence from SQK-PCB114.24')
arg = parser.parse_args()

adapter = arg.adapter[:arg.prefix]

polyA_hook = 'A' * arg.min_len + adapter
polyT_hook = korflab.anti(adapter) + 'T' * arg.min_len

print(f'>polyA_hook len{arg.min_len}_prefix{arg.prefix}')
print(polyA_hook)
print(f'>polyT_hook len{arg.min_len}_prefix{arg.prefix}')
print(polyT_hook)
