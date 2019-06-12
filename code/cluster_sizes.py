#!/usr/bin/env python

"""Prints cluster sizes and average to stdout"""

import argparse


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-c', '--clusters', type=str, help="File containing clusters")
    return parser.parse_args()


def main(args):
    clusters = {}
    with open(args.clusters, 'r') as fc:
        for line in fc:
            fields = line.strip().split('\t')
            if len(fields) == 1:
                cluster = int(fields[0])
            else:
                cluster = int(fields[1])
            clusters[cluster] = clusters.get(cluster, 0) + 1
    sum_sizes = 0
    for cluster in sorted(clusters.keys()):
        cluster_size = clusters[cluster]
        sum_sizes += cluster_size
        print("{}\t{}".format(cluster, cluster_size))
    print("")
    print("Mean cluster size {}".format(sum_sizes / len(clusters)))


if __name__ == '__main__':
    main(parse_args())
