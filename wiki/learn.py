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
        print globals()['__doc__'] % locals()
        sys.exit(1)
    inp, outp = sys.argv[1:3]

    # create a phrase detector to learn phrases
    bigram_transformer = Phrases(LineSentence(inp))
    model = Word2Vec(bigram_transformer, size=400, window=5, min_count=5, workers=multiprocessing.cpu_count())

    # trim unneeded model memory = use (much) less RAM
    # doing this results in a model that is not further trainable so don't do it here
    # model.init_sims(replace=True)

    model.save(outp)
