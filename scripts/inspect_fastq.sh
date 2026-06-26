#!/usr/bin/env bash
set -euo pipefail

FASTQ=${1:-data/1k.fastq.gz}

echo "Input: $FASTQ"
echo

echo "Read length stats"
zcat "$FASTQ" | awk '
NR%4==2 {
    n++
    len=length($0)
    sum+=len
    sumsq+=len*len
    if (len>max) max=len
}
END {
    mean=sum/n
    sd=sqrt(sumsq/n - mean*mean)
    print "reads", n
    print "mean", mean
    print "sd", sd
    print "max", max
}'
echo

echo "N50"
zcat "$FASTQ" | awk '
NR%4==2 {
    l[++n]=length($0)
    total+=l[n]
}
END {
    asort(l)
    half=total/2
    s=0
    for (i=n; i>=1; i--) {
        s+=l[i]
        if (s>=half) {
            print l[i]
            break
        }
    }
}'
echo

echo "Start/end >=20 A/T"
zcat "$FASTQ" | awk '
NR%4==2 {
    n++
    if ($0 ~ /A{20,}$/) endA++
    if ($0 ~ /^A{20,}/) startA++
    if ($0 ~ /T{20,}$/) endT++
    if ($0 ~ /^T{20,}/) startT++
}
END {
    c=endA+startA+endT+startT
    print "reads", n
    print "count", c
    print "fraction", c/n
}'
echo

echo "Anywhere >=20 A/T"
zcat "$FASTQ" | awk '
NR%4==2 {
    n++
    if ($0 ~ /A{20,}/) anyA++
    if ($0 ~ /T{20,}/) anyT++
    if ($0 ~ /A{20,}/ || $0 ~ /T{20,}/) anyAT++
}
END {
    print "reads", n
    print "A20", anyA, anyA/n
    print "T20", anyT, anyT/n
    print "A20_or_T20", anyAT, anyAT/n
}'
echo

echo "Example A-run with repeated flank"
zcat "$FASTQ" | awk '
NR%4==2 && $0 ~ /A{20,}CTTGCGGGCGGCG/ {
    match($0, /A{20,}CTTGCGGGCGGCG/)
    start=RSTART-30
    if (start<1) start=1
    print substr($0,start,120)
    exit
}'
