#!/usr/bin/env python3

import argparse
import os

parser = argparse.ArgumentParser(
	description='blast polyA/polyT hooks against reads to find candidate 3ends')
parser.add_argument('fastq', help='input fastq file')
parser.add_argument('--hooks', default='data/hooks.fa',
	help='hook query fasta [%(default)s]')
parser.add_argument('--build', default='build',
	help='build directory [%(default)s]')
parser.add_argument('--evalue', type=float, default=1e-10,
	help='e-value cutoff [%(default)g]')
parser.add_argument('--cpus', type=int, default=4, help='[%(default)i]')
arg = parser.parse_args()

os.system(f'mkdir -p {arg.build}')

reads_fa = f'{arg.build}/reads.fa'
if not os.path.exists(f'{reads_fa}.nsq'):
	os.system(f'python3 scripts/fastq2fasta.py {arg.fastq} > {reads_fa}')
	os.system(f'formatdb -p F -i {reads_fa}')

params = ' '.join((
	'-p blastn',
	f'-d {reads_fa}',
	f'-i {arg.hooks}',
	f'-a {arg.cpus}',
	'-F F',                     # turn off DUST filter
	f'-e {arg.evalue}',
	'-m 8',
))

out = f'{arg.build}/hooks_vs_reads.tsv'
os.system(f'blastall {params} > {out}')
print(f'output written to {out}')
