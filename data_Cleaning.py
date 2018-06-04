# -*- coding:utf-8 -*-
# -------------------------------------------------- #
#     Be the change you want to see in the world.    #
#     Author：Sambo Qin                              #
#     Tel：1777-637-6617                             #
#     Mail：muse824@outlook.com                      #
# -------------------------------------------------- #
import os
import numpy as np
import re
import jieba as ws
from yaafelib import FeaturePlan, Engine, AudioFileProcessor
from gensim import models, corpora
import logging
import subprocess

#----------------------------------#
#                                  #
#            音频特征提取            #
#                                  #
#----------------------------------#

def audio_trans(locltag):

    filepath = "/home/master/dataset/audio_m4a/"+locltag+"/"  # 添加源文件路径
    new_path = "/home/master/dataset/audio_wav/"+locltag+"/"  # 输出路径
    filename = os.listdir(filepath)  # 得到文件夹下的所有文件名称
    songpath = []
    for i in range(len(filename)):
        filename[i] = filepath+filename[i]
        songpath.append(filename[i])
    for i in range(0,len(songpath)):
        path, name = os.path.split(songpath[i])
        if name.split('.')[-1] != 'm4a':
            print ('Not a m4a file')
            continue
        if new_path is None or new_path.split('.')[-1] != 'wav':
            print(name.split('.')[0]+ '.wav')
            wav_path = os.path.join(new_path, name.split('.')[0] + '.wav')

            #error = subprocess.call(['ffmpeg', '-i', songpath[i],"-acodec","pcm_s16le", "-ac","1","-ar","44100", wav_path])
            error = subprocess.call(
                ['/usr/local/ffmpeg/bin/ffmpeg', '-i', songpath[i], "-acodec","pcm_s16le", "-ac","2","-ab","128","-ar","44100",wav_path])
            if error:
                print("error")
            print("第 %s 首歌曲正在转换，请稍后片刻......"%(i+1))
            print("%s 格式转换已完成！"%name)
    return new_path


#----------------------------------#
#                                  #
#            音频特征提取            #
#                                  #
#----------------------------------#

def init():

    global engine
    fp = FeaturePlan(sample_rate=44100, resample=True, time_start=0, time_limit=60)   # 采样率44.1Hkz，提取20 - 40s

    fp.addFeature("mfcc: MFCC")             # 梅尔倒谱系数 13
    fp.addFeature("energy: Energy")         # 短时能量 1
    fp.addFeature("zcr: ZCR")               # 短时平均过零率 1
    fp.addFeature("sf: SpectralFlux")       # 尖锐度 1
    fp.addFeature("sr: SpectralRolloff")    # 频谱滚降点 1
    fp.addFeature("lpc: LPC LPCNbCoeffs=3") # 线性预测编码 3
    fp.addFeature("lx: Loudness")           # 响度 24

    df = fp.getDataFlow()
    engine = Engine()                  # 配置Engine
    engine.load(df)

    return 'Yaafe初始化'

def startEngine(path):
    global afp, features
    afp = AudioFileProcessor()
    afp.processFile(engine,path)       # 从mp3文件中提取特征，它必需提供engine配置

    features = engine.readAllOutputs() # 得到所有特征矩阵

    return 'Yaafe提取成功'

#特征MFCC提取
def getMFCC(locltag):

    mfcc = features.get('mfcc')
    lx = features.get("lx")
    zcr = features.get('zcr')
    energy = features.get("energy")
    sf = features.get("sf")
    sr = features.get("sr")

    mfccMax = np.max(mfcc,axis=0).round(decimals=5)
    mfccMean = np.mean(mfcc,axis=0).round(decimals=5)
    mfccVar = np.var(mfcc,axis=0).round(decimals=5)
    mfccMed = np.median(mfcc,axis=0).round(decimals=5)

    lxVar = np.mean(lx,axis=0).round(decimals=5)
    lxMed = np.median(lx,axis=0).round(decimals=5)

    zcrMax = np.max(zcr,axis=0).round(decimals=5)
    zcrMean = np.mean(zcr,axis=0).round(decimals=5)
    zcrVar = np.var(zcr,axis=0).round(decimals=5)
    zcrMed = np.median(zcr, axis=0).round(decimals=5)

    energyMax = np.max(energy,axis=0).round(decimals=5)
    energyVar = np.mean(energy,axis=0).round(decimals=5)
    energyMed = np.median(energy,axis=0).round(decimals=5)

    srVar = np.mean(sr,axis=0).round(decimals=5)
    srMed = np.median(sr,axis=0).round(decimals=5)

    sfVar = np.mean(sf,axis=0).round(decimals=5)
    sfMed = np.median(sf,axis=0).round(decimals=5)


    all = [mfccMean, mfccVar, mfccMax, mfccMed, lxVar, lxMed,
           zcrMax, zcrMean, zcrVar, zcrMed, energyMax, energyVar, energyMed,srVar, srMed,sfVar,sfMed]
    print(all)
    with open("/home/master/dataset/audio_wav/audiofeature.csv","a+") as f:
        for i in range(len(all)):
            all[i] = [str(item) for item in all[i]]
            string = ",".join(all[i])
            f.write(string+",")
        # happy:1,lonely:2,miss:3,sad:4,sweet:5,vent:6,strive:7,quiet:8,cure:9
        # 写入类别
        f.write("%s"%locltag+"\n")
    return

#提取音频特征
def audio_features(locltag):

    #happy:1,lonely:2,miss:3,sad:4,sweet:5,vent:6,strive:7,quiet:8,cure:9
    #维度：120
    file_dir = "/home/master/dataset/audio_wav/"+locltag+"/"
    filename = os.listdir(file_dir)
    filepath = []

    for i in range(len(filename)):
        filename[i] = file_dir + filename[i]
        filepath.append(filename[i])


    for i in range(len(filename)):
        init()
        startEngine(filename[i])
        getMFCC(locltag)

#----------------------------------#
#                                  #
#            构建歌词预料库           #
#                                  #
#----------------------------------#

def corpus_lyric():
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
            # 写入本地
            dictFileName = '/home/master/dataset/lyric_corpus/'+locltag+'/audio_lyric.dict'
            corpusFileName = '/home/master/dataset/lyric_corpus/'+locltag+'/audio_lyric.mm'
            dictionary = corpora.Dictionary(documents)
            corpus = [dictionary.doc2bow(doc) for doc in documents]  # generate the corpus
            dictionary.save_as_text(dictFileName)
            file.close()



    corpora.MmCorpus.serialize(corpusFileName, corpus)
    tf_idf = models.TfidfModel(corpus)  # the constructor
    print 'Build corpus done'

    # this may convert the docs into the TF-IDF space.
    # Here will convert all docs to TFIDF
    corpus_tfidf = tf_idf[corpus]
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=9)
    topics=lsi.show_topics(num_words=10,log=0)
    for tpc in topics:
        print(tpc)
    return

if __name__ == '__main__':
    # happy 117/sad 52/sweet 59/miss 68/quiet 122/lonely 55/cure 116/vent 126/strive 125
    locltag = "quiet"
    #音频格式统一化
    audio_trans(locltag)
    #音频特征提取
    audio_features(locltag)
    #构建歌词语料库
    corpus_lyric()


