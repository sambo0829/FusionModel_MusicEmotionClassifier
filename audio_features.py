# -*- coding:utf-8 -*-
# -------------------------------------------------- #
#     Be the change you want to see in the world.    #
#     Author：Sambo Qin                              #
#     Tel：1777-637-6617                             #
#     Mail：muse824@outlook.com                      #
# -------------------------------------------------- #

import os
import numpy as np
from yaafelib import FeaturePlan, Engine, AudioFileProcessor

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
def getMFCC():

    mfcc = features.get('mfcc',{'Precision':'8'})
    lx = features.get("lx",{'Precision':'8'})
    lpc = features.get('lpc',{'Precision':'8'})
    zcr = features.get('zcr',{'Precision':'8'})
    energy = features.get("energy",{'Precision':'8'})
    sf = features.get("sf",{'Precision':'8'})
    sr = features.get("sr",{'Precision':'8'})

    mfccMax = np.max(mfcc,axis=0)
    mfccMean = np.mean(mfcc,axis=0)
    mfccVar = np.var(mfcc,axis=0)
    mfccMed = np.median(mfcc,axis=0)

    lxVar = np.mean(lx,axis=0)
    lxMed = np.median(lx,axis=0)

    lpcMean = np.mean(lpc,axis=0)
    lpcVar = np.var(lpc,axis=0)
    lpcMed = np.median(lpc, axis=0)

    zcrMax = np.max(zcr,axis=0)
    zcrMean = np.mean(zcr,axis=0)
    zcrVar = np.var(zcr,axis=0)
    zcrMed = np.median(zcr, axis=0)

    energyMax = np.max(energy,axis=0)
    energyVar = np.mean(energy,axis=0)
    energyMed = np.median(energy, axis=0)

    srVar = np.mean(sr,axis=0)
    srMed = np.median(sr, axis=0)

    sfVar = np.mean(sf,axis=0)
    sfMed = np.median(sf, axis=0)


    all = [mfccMean, mfccVar, mfccMax, mfccMed, lxVar, lxMed, lpcMean, lpcVar, lpcMed,
           zcrMax, zcrMean, zcrVar, zcrMed, energyMax, energyVar, energyMed,srVar, srMed,sfVar,sfMed]
    print(all)
    with open("/home/master/dataset/audio_wav/featureset.csv","a+") as f:
        for i in range(len(all)):
            all[i] = [str(item) for item in all[i]]
            string = ",".join(all[i])
            f.write(string+",")
        # happy:1,lonely:2,miss:3,sad:4,sweet:5,vent:6,strive:7,quiet:8,cure:9
        # 写入类别
        f.write("5"+"\n")
    return

#提取特征
def audio_features():

    #happy:1,lonely:2,miss:3,sad:4,sweet:5,vent:6,strive:7,quiet:8,cure:9
    #维度：120
    file_dir = "/home/master/dataset/audio_wav/sweet/"
    filename = os.listdir(file_dir)
    filepath = []

    for i in range(len(filename)):
        filename[i] = file_dir + filename[i]
        filepath.append(filename[i])


    for i in range(len(filename)):
        init()
        startEngine(filename[i])
        getMFCC()


if __name__ == '__main__':

    #音频特征提取
    audio_features()
