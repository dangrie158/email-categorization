#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os.path
import sys
import multiprocessing
import pickle

from gensim.corpora import  WikiCorpus
from gensim.models import LdaModel
from gensim.models.word2vec import LineSentence
from gensim.models import Phrases
from gensim import corpora

import numpy as np

from nltk.corpus import stopwords as sw
from nltk.stem.snowball import GermanStemmer


stemmer = GermanStemmer()
stopwords = sw.words('german')
# gensims LineSentence generator replaces umlauts with
# u, a or o so add these variants to the stopwordlist
for stopword in stopwords:
    stopword = stopword.replace(u'ü', 'u')
    stopword = stopword.replace(u'ö', 'o')
    stopword = stopword.replace(u'ä', 'a')
    if stopword not in stopwords:
        stopwords.append(stopword)

np.random.seed(0)

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments

    if len(sys.argv) < 3:
        print(__doc__ % sys.argv[0].split("/")[-1])
        sys.exit(1)
    inp, outp = sys.argv[1:3]

    # create a phrase detector to learn phrases
    sentence_iterator = LineSentence(inp)

    def StemmingIterator(sentences):
        for line in sentences:
            yield [stemmer.stem(x) for x in line if x not in stopwords]

    def create_corpus(sentences, dictionary):
        corpus = []
        i = 0
        for text in sentences:
            if i % 10000 == 0:
                logger.info('corpus creation at {}'.format(i))
            corpus.append(dictionary.doc2bow(text))
            i += 1
        return corpus


    stemming_iterator = StemmingIterator(sentence_iterator)

    # try to load the dict from file or learn a new dict
    dict_filename = outp + '.dict';
    dictionary = None
    try:
        print('loading dict from file {}'.format(dict_filename))
        dictionary = corpora.Dictionary.load(dict_filename)
    except:
        print('create new dict')
        dictionary = corpora.Dictionary(stemming_iterator)
        dictionary.save()

    corpus_filename = outp + '.corpus'
    corpus = None
    try:
        print('loading corpus from file {}'.format(corpus_filename))
        corpus = pickle.load(open(corpus_filename, 'rb'))
    except:
        print('create new corpus')
        corpus = create_corpus(stemming_iterator, dictionary)
        #pickle.dump(corpus, open(corpus_filename, 'wb'))

    model = LdaModel(corpus, num_topics=200, id2word = dictionary, passes=20, random_state=0)

    # trim unneeded model memory = use (much) less RAM
    # doing this results in a model that is not further trainable so don't do it here
    # model.init_sims(replace=True)

    model.save(outp)
