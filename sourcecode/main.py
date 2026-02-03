#!/usr/bin/env python3
"""Invoke Community Notes scoring and user contribution algorithms.

Example Usage:

# To download, preprocess and filter data files
 1. python data-processing.py 

 2. python main.py \
    --enrollment data/userEnrollment-00001.tsv \
    --notes data/notes-00001.tsv \
    --ratings data/ratings-00001.tsv \
    --status data/noteStatusHistory-00001.tsv \
    --outdir data
"""

from scoring.runner import main


if __name__ == "__main__":
  main()
