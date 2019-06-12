#!/usr/bin/env python

"""Sorts a file from gender_associations_hypotest.py in function of number of target words. Most words first."""

import argparse
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-t', '--tests', type=str, help="Tests file from gender_associations_hypotest.py")
    parser.add_argument('-o', '--out', type=str, help="Sorted results")
    return parser.parse_args()


def main(args):
    lines = []
    word_counts = []
    with open(args.tests, 'r') as f:
        for line in f:
            lines.append(line)
            fields = line.strip().split('\t')
            n_x = len(fields[3].split(','))
            n_y = len(fields[4].split(','))
            word_counts.append(n_x + n_y)
    indices = np.argsort(word_counts)[::-1]
    sorted_lines = [lines[i] for i in indices]
    with open(args.out, 'w') as fout:
        for line in sorted_lines:
            fout.write(line)


if __name__ == '__main__':
    main(parse_args())
