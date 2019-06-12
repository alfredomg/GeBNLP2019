#!/usr/bin/env python

"""Conducts gender association tests on a per cluster basis using means difference method (as per Caliskan et al 2017) --
Produces a file with results each cluster and each word within the cluster. It's a tab-separated file with the follwing contents:
CLUSTER    CLUSTER_DESC    WORD    ASSOCIATED_GENDER    GENDER_SCORE

where:
CLUSTER is cluster number.
CLUSTER_DESC is a 'description' of the cluster based on the 10 words nearest to the cluster centroid.
WORD is the word in being tested for assiciations
ASSOCIATED_GENDER is the gender (M/F) to which the WORD tends to associate
GENDER_SCORE is the association value -- negative values are more female than positive values
"""

import argparse
import gensim
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-v', '--vectors', type=str, help="File containing Word Embeddings")
    parser.add_argument('-t', '--type', choices=['w2v', 'ft'], default='w2v',
                        help='Type of Word Embedding: w2v: word2vec, ft: fasttext')
    parser.add_argument('-c', '--clusters', type=str, help="Clustering file")
    parser.add_argument('-f', '--fattr', type=str, help="Female Attribute words list, one word per line")
    parser.add_argument('-m', '--mattr', type=str, help="Male Attribute words list, one word per line")
    parser.add_argument('-o', '--out', type=str, help="Output to save results of tests (one line per test)")
    return parser.parse_args()


def main(args):
    if args.type == 'w2v':
        wv = gensim.models.KeyedVectors.load_word2vec_format(args.vectors, binary=True, unicode_errors='ignore')
    elif args.type == 'ft':
        wv = gensim.models.fasttext.load_facebook_vectors(args.vectors)
    else:
        raise ValueError("Unsupported Word Embedding type '{}'".format(args.type))

    female_attrs = filter_words(wv, load_attrs(args.fattr))
    male_attrs = filter_words(wv, load_attrs(args.mattr))
    cluster2word = load_clusters(args.clusters, wv.vocab)
    with open(args.out, 'w') as fout:
        for cluster in sorted(cluster2word.keys()):
            cluster_words = cluster2word[cluster]
            cluster_desc = get_cluster_description(wv, cluster_words)
            for word in cluster_words:
                score = cosine_means_difference(wv, word, male_attrs, female_attrs)
                gender = 'F' if score < 0 else 'M'
                fout.write("{}\t{}\t{}\t{}\t{}\n".format(cluster, cluster_desc, word, gender, score))
    print("Done!")


def cosine_means_difference(wv, word, male_attrs, female_attrs):
    male_mean = cosine_mean(wv, word, male_attrs)
    female_mean = cosine_mean(wv, word, female_attrs)
    return male_mean - female_mean


def cosine_mean(wv, word, attrs):
    return wv.cosine_similarities(wv[word], [wv[w] for w in attrs]).mean()


def get_cluster_description(wv, cluster_words):
    cluster_centroid = wv[cluster_words].sum(axis=0) / len(cluster_words)
    most_similars = wv.similar_by_vector(cluster_centroid.T, topn=10)
    words = [elem[0] for elem in most_similars]
    return ','.join(words)


def load_clusters(cluster_file, vocab):
    cluster2word = {}
    with open(cluster_file, 'r') as fclus:
        for line in fclus:
            fields = line.strip().split('\t')
            if len(fields) != 2:
                continue
            else:
                word = fields[0]
                cluster = int(fields[1])
            if word not in vocab:
                continue
            cluster_rec = cluster2word.get(cluster, None)
            if cluster_rec is None:
                cluster_rec = []
                cluster2word[cluster] = cluster_rec
            cluster_rec.append(word)
    return cluster2word


def filter_words(wv, words):
    final_words = []
    for word in words:
        if word in wv.vocab:
            final_words.append(word)
    return final_words


def load_attrs(path):
    text = open(path, "r")
    text_list = list(set(text.read().splitlines()))
    return text_list


if __name__ == '__main__':
    main(parse_args())
