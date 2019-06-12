#!/usr/bin/env python

"""Conducts hypothesis tests on specific target word lists (cases).
Main input is a text file with following format:
NAME    X    Y
where:
NAME - Arbitrary name for case (category)
X - path to X target word list
Y - path to Y target word list
-----
Output:
Produces file with following format
NAME    P-VALUEi    COHENS_Di
where
NAME is case name from input file
P-VALUEi is the hypothesis p-value for ith case (category) test
COHENS_Di is the Cohen's d statistic for the ith case (category) test
"""

import argparse
import gensim
import gender_associations as ga
import gender_associations_hypotest as gah


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-v', '--vectors', type=str, help="File containing Word Embeddings")
    parser.add_argument('-t', '--type', choices=['w2v', 'ft'], default='w2v',
                        help='Type of Word Embedding: w2v: word2vec, ft: fasttext')
    parser.add_argument('-f', '--fattr', type=str, help="Female Attribute words list, one word per line")
    parser.add_argument('-m', '--mattr', type=str, help="Male Attribute words list, one word per line")
    parser.add_argument('-i', '--iter', type=int, default=1000, help="Number of iterations on each randomisation test")
    parser.add_argument('-c', '--cases', type=str, help="Input file containing cases")
    parser.add_argument('-o', '--out', type=str, help="Output to save results of tests (one line per test)")
    return parser.parse_args()


def main(args):
    if args.type == 'w2v':
        wv = gensim.models.KeyedVectors.load_word2vec_format(args.vectors, binary=True, unicode_errors='ignore')
    elif args.type == 'ft':
        wv = gensim.models.fasttext.load_facebook_vectors(args.vectors)
    else:
        raise ValueError("Unsupported Word Embedding type '{}'".format(args.type))

    f_attrs = ga.filter_words(wv, ga.load_attrs(args.fattr))
    m_attrs = ga.filter_words(wv, ga.load_attrs(args.mattr))
    with open(args.cases, 'r') as fc, open(args.out, 'w') as fout:
        for case in fc:
            fields = case.strip().split('\t')
            name = fields[0]
            x_targets_file = fields[1]
            x_targets = ga.filter_words(wv, ga.load_attrs(x_targets_file))
            y_targets_file = fields[2]
            y_targets = ga.filter_words(wv, ga.load_attrs(y_targets_file))
            p_value = gah.weat_rand_test(wv, x_targets, y_targets, m_attrs, f_attrs, args.iter)
            cohens_d = gah.get_cohens_d(wv,  x_targets, y_targets, m_attrs, f_attrs)
            fout.write("{}\t{}\t{}\n".format(name, p_value, cohens_d))
    print("Done!")


if __name__ == '__main__':
    main(parse_args())
