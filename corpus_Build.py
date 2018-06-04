# -*- coding:utf-8 -*-
# -------------------------------------------------- #
#     Be the change you want to see in the world.    #
#     Author：Sambo Qin                              #
#     Tel：1777-637-6617                             #
#     Mail：muse824@outlook.com                      #
# -------------------------------------------------- #

import os
import re
import jieba as ws
from gensim import models, corpora
import logging

def corpus_build():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    documents = []
    labels = []
    class_dir = os.listdir('/home/master/dataset/audio_lyric/')
    r1 = u'[a-zA-Z0-9\'’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】：《》？“”‘’！[\\]^_`{|}~[\n]]+'
    # 读取语料库
    for i in class_dir:
        currentpath = '/home/master/dataset/audio_lyric/' + i + '/'
        #print(currentpath)
        files = os.listdir(currentpath)
        for f in files:
            tmp_list = []
            tmp_str = ''
            try:
                file = open(currentpath + f, "r+")
                file_str = file.read()
                file_str = re.sub(r1, '', file_str)  # 正则处理，去掉一些噪音

                doc = ''.join(file_str)

                tmp_str = '|'.join(ws.cut(doc))

                tmp_list = tmp_str.split('|')

            except:
                print('read error: ' + currentpath + f)
            documents.append(tmp_list)
            file.close()

# ------------------------------------------------------------------------------
# LSI model: latent semantic indexing model
# ------------------------------------------------------------------------------
# https://en.wikipedia.org/wiki/Latent_semantic_analysis
# http://radimrehurek.com/gensim/wiki.html#latent-semantic-analysis
# print(documents)


    dictFileName = '/home/master/dataset/dict/audio_lyric.dict'
    corpusFileName = '/home/master/dataset/corpus/audio_lyric.mm'

    dictionary = corpora.Dictionary(documents)
    corpus = [dictionary.doc2bow(doc) for doc in documents]  # generate the corpus

    dictionary.save_as_text(dictFileName)
    corpora.MmCorpus.serialize(corpusFileName, corpus)
    tf_idf = models.TfidfModel(corpus)  # the constructor

    # this may convert the docs into the TF-IDF space.
    # Here will convert all docs to TFIDF
    corpus_tfidf = tf_idf[corpus]
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=9)
    topics=lsi.show_topics(num_words=10,log=0)
    for tpc in topics:
        print(tpc)
    return

if __name__ == '__main__':
    # train the lsi model
    corpus_build()

    print 'Build corpus done'
