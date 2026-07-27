# hmm-3end

Exploring mRNA 3′-end sequence architecture and poly(A)-associated signals toward a Hidden Markov Model (HMM) for 3′-end identification.

## Overview

This repository contains exploratory analyses and prototype scripts for studying mRNA 3′ ends from long-read sequencing data. The long-term goal is to develop an HMM capable of recognizing the sequence architecture surrounding transcript cleavage and poly(A) sites.

Current work focuses on identifying candidate 3′-end reads by detecting long poly(A) or poly(T) homopolymers in Nanopore sequencing data. These candidate sequences will later be used to guide HMM design and evaluation.

---

## Repository structure

```
hmm-3end/
├── README.md
├── data/
├── dummy_3end.json
├── envs/
├── notebooks/
├── scripts/
└── shell/
```

### data/

Small datasets used for development and testing.

Current primary test dataset:

```
data/1k.fastq.gz
```

Current output from the preprocessing script:

```
data/temp/pre1k.fa
```

### scripts/

Python scripts for preprocessing and exploratory analyses.

Current primary script:

```
scripts/preliminaryA.py
```

This script

- scans FASTQ reads for long poly(A) or poly(T) homopolymers,
- reverse-complements poly(T) candidates,
- extracts transcript-side sequence adjacent to the homopolymer,
- classifies reads into:

```
keep
both
neither
short
```

The `draft/` directory contains earlier prototype scripts preserved as development history.

### notebooks/

Interactive QC and exploratory analyses.

Currently contains:

```
qcfastq.ipynb
```

which provides notebook versions of analyses such as read-length and transcript-length summaries.

### envs/

Contains Conda environments.

Current environment:

```
env1.yml
```

### shell/

Shell scripts for future batch execution across multiple FASTQ files.

### dummy_3end.json

Prototype description of the planned Hidden Markov Model.

This file represents the conceptual HMM architecture and is intended for model development rather than sequence preprocessing.

---

## Current workflow

```
FASTQ
   │
   ▼
preliminaryA.py
   │
   ▼
candidate 3′-end FASTA
   │
   ▼
manual inspection
   │
   ▼
HMM design
   │
   ▼
future 3′-end prediction
```

---

# Environment Setup

## 1. Create the Conda environment

```bash
conda env create -f envs/env1.yml
```

## 2. Activate the environment

```bash
conda activate 3end
```

## 3. Register the Jupyter kernel

```bash
python -m ipykernel install \
    --user \
    --name 3end \
    --display-name "3end"
```

This only needs to be done once.

## 4. Open VS Code

```bash
code .
```

Open a notebook (`.ipynb`), click **Select Kernel**, and choose **3end**.

Verify the notebook is using the correct interpreter:

```python
import sys
print(sys.executable)
```

The output should point to the Python executable inside the `3end` Conda environment.