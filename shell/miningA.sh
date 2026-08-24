#!/usr/bin/env bash

set -e

inputdir=$1
outdir=$2
jobs=$3

if [ ! -d "$inputdir" ]; then
	echo "input directory not found: $inputdir" >&2
	exit 1
fi

if [ ! -d "$outdir" ]; then
	echo "output directory not found: $outdir" >&2
	exit 1
fi

nfiles=$(find "$inputdir" -maxdepth 1 -name '*.fastq.gz' | wc -l)

if [ "$nfiles" -eq 0 ]; then
	echo "no fastq.gz files found in: $inputdir" >&2
	exit 1
fi

rm -f "$outdir/mined.fa.gz"
rm -f "$outdir"/*.chunk.fa.gz

start=$(date +%s)

echo "FASTQ files	$nfiles" >&2
echo "parallel jobs	$jobs" >&2
echo "running..." >&2

find "$inputdir" -maxdepth 1 -name '*.fastq.gz' -print0 |
xargs -0 -r -P "$jobs" -I{} bash -o pipefail -c '
	file="$1"
	outdir="$2"

	name=$(basename "$file" .fastq.gz)

	python3 scripts/miningA.py "$file" |
	gzip > "$outdir/${name}.chunk.fa.gz"
' _ {} "$outdir"

cat "$outdir"/*.chunk.fa.gz > "$outdir/mined.fa.gz"
rm -f "$outdir"/*.chunk.fa.gz

end=$(date +%s)
elapsed=$((end - start))

echo "finished" >&2
echo "elapsed seconds	$elapsed" >&2
echo "output	$outdir/mined.fa.gz" >&2