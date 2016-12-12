#!/bin/sh
set -e

#preproces the wiki corpus
#python wiki/preprocess.py wiki/data/wiki.de.xml.bz2 wiki/data/wiki.de.txt

#learn the base model based on the wikipedia corpus
#python wiki/learn.py wiki/data/wiki.de.txt wiki/data/wiki.de.word2vec.model

# create the corpora for all hdm and non-hdm mails
#python mail/preprocess.py mail/data/all.mbox mail/data/hdm.txt hdm-stuttgart.de
#python mail/preprocess.py mail/data/all.mbox mail/data/non-hdm.txt \!hdm-stuttgart.de

# split corpora into validation and training data
#python mail/generateSets.py mail/data/hdm.txt mail/data/hdm.training.txt mail/data/hdm.validation.txt 100 0
#python mail/generateSets.py mail/data/non-hdm.txt mail/data/non-hdm.training.txt mail/data/non-hdm.validation.txt 100 0

# create extra models for the hdm and non hdm corpus based on the wiki corpus
#python mail/continueLearn.py wiki/data/wiki.de.word2vec.model mail/data/hdm.training.txt mail/data/hdm+base.word2vec.model
#python mail/continueLearn.py wiki/data/wiki.de.word2vec.model mail/data/non-hdm.training.txt mail/data/non-hdm+base.word2vec.model

# learn models on the mail corpora without the base model
#python wiki/learn.py mail/data/hdm.txt mail/data/hdm.word2vec.model
#python wiki/learn.py mail/data/non-hdm.txt mail/data/non-hdm.word2vec.model

# start local ongod to port foward before ssh before starting this
# ssh -L 27017:localhost:27017 root@nupo-artworks.de

python news/preprocess.py ../Wiki/news/corpus/ corpus

python mail/continueLearn.py wiki/data/wiki.de.word2vec.model news/corpus/corpusSonstiges.txt news/data/corpusSonstiges+base.word2vec.model
python mail/continueLearn.py wiki/data/wiki.de.word2vec.model news/corpus/corpusAktuell.txt news/data/corpusAktuell+base.word2vec.model
python mail/continueLearn.py wiki/data/wiki.de.word2vec.model news/corpus/corpusLifestyle.txt news/data/corpusLifestyle+base.word2vec.model
python mail/continueLearn.py wiki/data/wiki.de.word2vec.model news/corpus/corpusWirtschaft.txt news/data/corpusWirtschaft+base.word2vec.model
python mail/continueLearn.py wiki/data/wiki.de.word2vec.model news/corpus/corpusFinanzen.txt news/data/corpusFinanzen+base.word2vec.model
python mail/continueLearn.py wiki/data/wiki.de.word2vec.model news/corpus/corpusAusland.txt news/data/corpusAusland+base.word2vec.model
python mail/continueLearn.py wiki/data/wiki.de.word2vec.model news/corpus/corpusIgnore.txt news/data/corpusIgnore+base.word2vec.model
python mail/continueLearn.py wiki/data/wiki.de.word2vec.model news/corpus/corpusLokal.txt news/data/corpusLokal+base.word2vec.model
python mail/continueLearn.py wiki/data/wiki.de.word2vec.model news/corpus/corpusPolitik.txt news/data/corpusPolitik+base.word2vec.model
python mail/continueLearn.py wiki/data/wiki.de.word2vec.model news/corpus/corpusSport.txt news/data/corpusSport+base.word2vec.model
python mail/continueLearn.py wiki/data/wiki.de.word2vec.model news/corpus/corpusTechnologie.txt news/data/corpusTechnologie+base.word2vec.model
python mail/continueLearn.py wiki/data/wiki.de.word2vec.model news/corpus/corpusKultur.txt news/data/corpusKultur+base.word2vec.model

#python wiki/learn.py news/data/news.txt news/data/news.word2vec.model
#python mail/continueLearn.py wiki/data/wiki.de.word2vec.model news/data/news.txt news/data/news+base.word2vec.model
