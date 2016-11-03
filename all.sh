#!/bin/sh

#preproces the wikki corpus
#python wiki/preprocess.py wiki/data/wiki.de.xml.bz2 wiki/data/wiki.de.txt

#learn the base model based on the wikipedia corpus
python wiki/learn.py wiki/data/wiki.de.txt wiki/data/wiki.de.word2vec.model

# create the corpora for all hdm and non-hdm mails
#python mail/preprocess.py mail/data/all.mbox mail/data/hdm.txt hdm-stuttgart.de
#python mail/preprocess.py mail/data/all.mbox mail/data/non-hdm.txt \!hdm-stuttgart.de

# split corpora into validation and training data
#python mail/generateSets.py mail/data/hdm.txt mail/data/hdm.training.txt mail/data/hdm.validation.txt 30 0
#python mail/generateSets.py mail/data/non-hdm.txt mail/data/non-hdm.training.txt mail/data/non-hdm.validation.txt 30 0
