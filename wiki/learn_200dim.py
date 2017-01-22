#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os.path
import sys
import multiprocessing

from gensim.corpora import  WikiCorpus
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
from gensim.models import Phrases


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

    # phrase detection is already done in the preprocess stage
    # bigram_transformer = Phrases(sentence_iterator)
    # hs=1: use hierarchical softmax so we can use the availabe score function of the model
    model = Word2Vec(sentence_iterator, size=200, window=5, min_count=5, workers=multiprocessing.cpu_count(), hs=1)

    # trim unneeded model memory = use (much) less RAM
    # doing this results in a model that is not further trainable so don't do it here
    # model.init_sims(replace=True)

    model.save(outp)
