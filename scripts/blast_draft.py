#!/usr/bin/env python3

import argparse
import os

parser = argparse.ArgumentParser(
	description='blast polyA hook against reads to find candidate 3end junctions')
parser.add_argument('fastq', help='input fastq file')
parser.add_argument('--hooks',  default='data/hooks.fa', metavar='<file.fa>',
	help='hook query fasta [%(default)s]')
parser.add_argument('--build',  default='build', metavar='<dir>',
	help='build directory [%(default)s]')
parser.add_argument('--evalue', type=float, default=1e-5, metavar='<float>',
	help='e-value cutoff [%(default)g]')
parser.add_argument('--max-targets', type=int, default=1000000, metavar='<int>',
	help='reads reported per hook [%(default)i]')
arg = parser.parse_args()

os.system(f'mkdir -p {arg.build}')

reads_fa = f'{arg.build}/reads.fa'
if not os.path.exists(f'{reads_fa}.nsq'):
	os.system(f'python3 scripts/fastq2fasta.py {arg.fastq} > {reads_fa}')
	os.system(f'makeblastdb -in {reads_fa} -dbtype nucl')

params = ' '.join((
	'-task blastn',                        # megablast seeds on 28 nt, hook is 35
	f'-db {reads_fa}',
	f'-query {arg.hooks}',
	'-dust no',                            # hook is mostly homopolymer
	f'-evalue {arg.evalue}',
	f'-max_target_seqs {arg.max_targets}', # default 500 truncates silently
))

for fmt, ext in (('0', 'txt'), ('6', 'tsv')):
	out = f'{arg.build}/blast.{ext}'
	os.system(f'blastn {params} -outfmt {fmt} > {out}')
	print('wrote', out)