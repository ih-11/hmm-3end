#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description='generate polyA hook for blast')
parser.add_argument('--min-len', type=int, default=15, help='A/T run length')
parser.add_argument('--prefix',  type=int, default=20, help='adapter prefix length')
parser.add_argument('--adapter',
	default='CTTGCGGGCGGCGGACTCTCCTCTGAAGATAGAGCGACAGGCAAG',
	help='CRTA sequence from SQK-PCB114.24')
arg = parser.parse_args()

adapter = arg.adapter[:arg.prefix]
hook    = 'A' * arg.min_len + adapter

print(f'>polyA_hook run={arg.min_len} prefix={arg.prefix}')
print(hook)