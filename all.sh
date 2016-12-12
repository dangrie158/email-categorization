#!/bin/sh
set -e

#download the wiki corpus
#curl -o wiki/data/wiki.de.xml.bz2 https://dumps.wikimedia.org/dewiki/latest/dewiki-latest-pages-articles.xml.bz2

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

# start local mongod or port foward before ssh before starting the preprocessor
# ssh -L 27017:localhost:27017 root@nupo-artworks.de

#python news/preprocess.py ../Wiki/news/corpus/ corpus

categories=( "Sonstiges" "Aktuell" "Lifestyle" "Wirtschaft" "Finanzen" "Ausland" "Lokal" "Politik" "Sport" "Technologie" "Kultur")

for i in "${categories[@]}"
do
  #split the corpus into 2 sets with a ratio of 70% training / 30% validation
  python mail/generateSets.py news/corpus/corpus$i.txt news/data/corpus$i.training.txt news/data/corpus$i.validation.txt 30 0
  python mail/continueLearn.py wiki/data/wiki.de.word2vec.model news/data/corpus$i.training.txt news/data/corpus$i+base.word2vec.model
done

#python wiki/learn.py news/data/news.txt news/data/news.word2vec.model
#python mail/continueLearn.py wiki/data/wiki.de.word2vec.model news/data/news.txt news/data/news+base.word2vec.model
