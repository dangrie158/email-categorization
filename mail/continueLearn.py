#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage: %s basemodel extended_trainingset save_path

Continue lerning a basemodel with extra training data and save the new
model to save_path
"""

import logging
import os.path
import sys
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments

    if len(sys.argv) < 4:
        print(__doc__ % sys.argv[0].split("/")[-1])
        sys.exit(1)
    basemodel_path, train_data, save_path = sys.argv[1:4]

    print('extending basemodel from {} with new training data from {}'.format(basemodel_path, train_data))

    print('loading basemodel from {}'.format(basemodel_path))
    base_model = Word2Vec.load(basemodel_path)

    print('loading training data to extend model')
    sentence_iterator = LineSentence(train_data)

    print('learning basemodel with new data')
    base_model.train(sentence_iterator)

    #print('precomputing L2 normalized vectors of new model')
    #base_model.init_sims(replace=True)

    print('saving base model to new file')
    base_model.save(save_path)

    print('done')
    print('')
