#!/usr/bin/env python

"""Clusters word embeddings based on K-Means. Output is a tab-separated text file:
WORD   CLUSTER"""

import argparse
import gensim
from sklearn.cluster import MiniBatchKMeans


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-v', '--vectors', type=str, help="File containing Word Embeddings")
    parser.add_argument('-t', '--type', choices=['w2v', 'ft'], default='w2v',
                        help='Type of Word Embedding: w2v: word2vec, ft: fasttext')
    parser.add_argument('-k', '--k', type=int, default=10, help='Number of clusters')
    parser.add_argument('-b', '--bs', type=int, default=100, help='Batch size')
    parser.add_argument('-o', '--out', type=str, help="Output to save results of tests (one line per test)")
    return parser.parse_args()


def main(args):
    if args.type == 'w2v':
        wv = gensim.models.KeyedVectors.load_word2vec_format(args.vectors, binary=True, unicode_errors='ignore')
    elif args.type == 'ft':
        wv = gensim.models.fasttext.load_facebook_vectors(args.vectors)
    else:
        raise ValueError("Unsupported Word Embedding type '{}'".format(args.type))

    mbk = MiniBatchKMeans(init='k-means++', n_clusters=args.k, batch_size=args.bs, max_no_improvement=10, verbose=0)
    mbk.fit(wv.vectors)

    with open(args.out, 'w') as fout:
        for word, cluster in zip(wv.vocab, mbk.labels_):
            fout.write("{}\t{}\n".format(word, cluster))
    print("Done!")


if __name__ == '__main__':
    main(parse_args())
