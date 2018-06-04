# -*- coding:utf-8 -*-
# -------------------------------------------------- #
#     Be the change you want to see in the world.    #
#     Author：Sambo Qin                              #
#     Tel：1777-637-6617                             #
#     Mail：muse824@outlook.com                      #
# -------------------------------------------------- #
import os
from gensim import corpora, models, similarities
import sys
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')

def getFileList(dir):
    return [dir + x for x in os.listdir(dir)]


dictLists = getFileList('/home/master/dataset/dict/')


class LoadDictionary(object):
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def __iter__(self):
        for dictFile in dictLists:
            sFileRaw, sFilePostfix = os.path.splitext(dictFile)
            sFileDir, sFileName = os.path.split(sFileRaw)
            (dictFile, corpusFile) = ('/home/master/dataset/dict/' + sFileName + '.dict', '/home/master/dataset/corpus/' + sFileName + '.mm')
            yield self.dictionary.load_from_text(dictFile)


class LoadCorpus(object):

    def __iter__(self):
        for dictFile in dictLists:
            sFileRaw, sFilePostfix = os.path.splitext(dictFile)
            sFileDir, sFileName = os.path.split(sFileRaw)
            (dictFile, corpusFile) = ('/home/master/dataset/dict/' + sFileName + '.dict', '/home/master/dataset/corpus/' + sFileName + '.mm')
            yield corpora.MmCorpus(corpusFile)


""" 
    预处理(easy_install nltk) 
"""


# 简化的 中文+英文 预处理
def pre_process_cn(inputs, low_freq_filter=True):
    """
        1.去掉停用词
        2.去掉标点符号
        3.处理为词干
        4.去掉低频词

    """
    import nltk
    import jieba.analyse
    from nltk.tokenize import word_tokenize

    texts_tokenized = []
    for document in inputs:
        texts_tokenized_tmp = []
        for word in word_tokenize(document):
            texts_tokenized_tmp += jieba.analyse.extract_tags(word, 10)
        texts_tokenized.append(texts_tokenized_tmp)

    texts_filtered_stopwords = texts_tokenized

    # 去除标点符号/英文字符
    english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%',
                            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                            'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                            's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
                            ]
    texts_filtered = [[word for word in document if not word in english_punctuations] for document in
                      texts_filtered_stopwords]

    # 词干化
    from nltk.stem.lancaster import LancasterStemmer
    st = LancasterStemmer()
    texts_stemmed = [[st.stem(word) for word in docment] for docment in texts_filtered]

    # 去除过低频词
    if low_freq_filter:
        all_stems = sum(texts_stemmed, [])
        stems_once = set(stem for stem in set(all_stems) if all_stems.count(stem) == 1)
        texts = [[stem for stem in text if stem not in stems_once] for text in texts_stemmed]
    else:
        texts = texts_stemmed
    return texts


dictionary = corpora.dictionary.Dictionary()
dictionary_memory_friendly = LoadDictionary(dictionary)
for vector in dictionary_memory_friendly:
    dictionary = vector

corpus = []
corpus_memory_friendly = LoadCorpus()
for vector in corpus_memory_friendly:
    corpus.append(vector[0])

if 0 < len(corpus):
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    model = models.LsiModel(corpus_tfidf, id2word=None, num_topics=20,
                            chunksize=2000000)  # 不指定 id2word=dictionary 时，LsiModel内部会根据 corpus 重建 dictionary
    index = similarities.Similarity('./novel_', model[corpus], num_features=len(corpus))

    # 要处理的对象登场，这里随便从小说中截取了一段话
    target_courses = ['男人们的脸上沉重而冷凝，蒙着面纱的女人们则是发出断断续续的哭泣声，他们无比专注地看着前方，见证一场生与死的拉锯战。']
    target_text = pre_process_cn(target_courses, low_freq_filter=False)

    """ 
    对具体对象相似度匹配 
    """
    # 选择一个基准数据
    ml_course = target_text[0]
    # 词袋处理
    ml_bow = dictionary.doc2bow(ml_course)

    # 在上面选择的模型数据 lsi model 中，计算其他数据与其的相似度
    ml_lsi = model[ml_bow]  # ml_lsi 形式如 (topic_id, topic_value)
    sims = index[ml_lsi]  # sims 是最终结果了， index[xxx] 调用内置方法 __getitem__() 来计算ml_lsi

    # 排序，为输出方便
    sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])

    # 查看结果
    print sort_sims[0:10]
    print len(dictLists)
    print dictLists[sort_sims[1][0]]
    print dictLists[sort_sims[2][0]]
    print dictLists[sort_sims[3][0]]