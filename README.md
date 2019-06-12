# GeBNLP2019

Accompanying code and data to the paper "Measuring Gender Bias in Word Embeddings across Domains and
Discovering New Gender Bias Word Categories" by Kaytlin Chaloner and Alfredo Maldonado. The paper will be presented at the 1st ACL Workshop on Gender Bias for Natural Language Processing 2019 in Florence.

## Citation

If you use this code, data or our results, we would appreciate if you could cite this paper as follows:

Kaytlin Chaloner and Alfredo Maldonado (2019). Measuring Gender Bias in Word Embeddings across Domains and Discovering New Gender Bias Word Categories. In Proceedings of the 1st ACL Workshop on Gender Bias for Natural Language Processing. Florence.

BibTeX:

```
@inproceedings{Chaloner2019,
address = {Florence},
author = {Chaloner, Kaytlin and Maldonado, Alfredo},
booktitle = {Proceedings of the 1st ACL Workshop on Gender Bias for Natural Language Processing},
title = {{Measuring Gender Bias in Word Embeddings across Domains and Discovering New Gender Bias Word Categories}},
year = {2019}
}
```

## Code

All code needed (barring standard installable dependencies) to run experiments is under the `code` directory.

Each script is documented with instructions on how to run it. You can also type `$ <script_name.py> --help` in a Linux terminal to obtain instructions on how to run the script.

## Data

This data is located inside the `data` directory:

* `weat_lists`: Standard weat word category lists (B1-B5 in the paper).

*  `all-cases.txt`: WEAT hypothesis tests P-values (100,000 iterations) and Cohen d's for each set of word embeddings on each of the five standard gender bias word categories (B1-B5).

The rest of the data is located at our <a target='_blank' href='https://drive.google.com/drive/folders/13HSQXJgCSYCgpf1tV3sC37bivCjySP2Q?usp=sharing'>public Google Drive Folder</a>:

* `gap-full.bin`: GAP Word Embeddings trained using FastText by ourselves. Can be loaded in Python using Gensim.

* `*.assocs`: Tab-separated files containing showing the bias association (measured by eq. 2 in paper) for each word in each cluster. Columns (fields) are:

	* `CLUSTER` -- cluster number.
	* `CLUSTER_DESC` -- a 'description' of the cluster based on the 10 words nearest to the cluster centroid.
	* `WORD` -- the word in being tested for associations.
	* `ASSOCIATED_GENDER` -- the gender (M/F) to which the `WORD` tends to associate.
	* `GENDER_SCORE` -- the association value. Negative values are more female than positive values.

	Each file corresponds to a different corpus/embedding set, as follows:

	* `gap-full.assocs` -- GAP Corpus
	* `GoogleNews-vectors-negative300.assocs` -- Google News
	* `word2vec_twitter_model.assocs` -- Twitter
	* `PubMed-shuffle-win-30.assocs` -- PubMed context window size 30

* `*.hypo-n20-1k.sorted`: These files contain the output of the New Gender Bias Word Discovery based on word clustering. They are tab-separated files containing the following columns (fields):

	* `CLUSTER` -- cluster number.
	* `MAJ_ASSOC` -- majority associated gender in cluster -- ie the gender with most associated words in gender_associations.py
	* `CLUSTER_DESC` -- a 'description' of the cluster based on the 10 words nearest to the cluster centroid.
	* `X_TARGETS` -- the n male-associated target words selected for the test
	* `Y_TARGETS` -- the n female-associated target words selected for the test
	* `P-VALUE` -- the hypothesis p-value (probability the Ho is true -- that there is no difference between `X_TARGETS` and `Y_TARGETS`  in their bias towards male or female attribute terms)
	* `COHENS_D` is Cohen's d statistic, i.e. the effect size (Caliskan et al: difference between two means divided by the standard deviation. "Conventional small, medium and large values of d are 0.2, 0.5 and 0.8, respectively".)

	Each file corresponds to a different corpus/embedding set, as follows:

	* `gap-full.hypo-n20-1k.sorted` -- GAP Corpus
	* `GoogleNews-vectors-negative300.hypo-n20-1k.sorted` -- Google News
	* `word2vec_twitter_model.hypo-n20-1k.sorted` -- Twitter
	* `PubMed-shuffle-win-30.hypo-n20-1k.sorted` -- PubMed context window size 30

	We also supply simplified versions of these files in LibreOffice format (.ods) for easier display on desktop/laptop computers.

	See paper for information on where to find these embeddings online.
