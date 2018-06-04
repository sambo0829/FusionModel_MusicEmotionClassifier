# -*- coding:utf-8 -*-
# -------------------------------------------------- #
#     Be the change you want to see in the world.    #
#     Author: Sambo Qin                              #
#     Tel: 1777-637-6617                             #
#     Mail: muse824@outlook.com                      #
# -------------------------------------------------- #
import numpy as np
import pandas as pd
from sklearn import svm
from sklearn.pipeline import Pipeline
from sklearn.datasets import load_files
from sklearn import metrics
from sklearn.externals import joblib
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

def Lyric_model():

    #标签分类
    categories = ['happy', 'lonely',
                  'sad', 'sweet', 'quiet',"vent","strive","cure","miss"]
    # 从硬盘获取训练数据# 从硬盘获取测试数据
    lyric_test = load_files('/home/master/dataset/lyric_test',
                            categories=categories,
                            load_content=True,
                            encoding='utf-8',
                            decode_error='strict',
                            shuffle=True, random_state=42)
    #训练模型
    print('基于歌词的音乐情感分类器 : \r')

def load_csv_data(filename):
    data = []
    labels = []
    datafile = open(filename)
    for line in datafile:
        fields = line.strip().split(',')
        data.append([float(field) for field in fields[:-1]])
        labels.append(fields[-1])
    data = np.array(data)
    labels = np.array(labels)
    return data, labels


def accuracy(test_labels, pred_lables):
    correct = np.sum(test_labels == pred_lables)
    n = len(test_labels)
    return float(correct) / n

def Audio_model():

    features, labels = load_csv_data('/home/master/dataset/audio_wav/featureset.csv')

    print('基于音频的音乐情感分类器 : \r')
    # 加载模型
    predicted_clf = joblib.load("music_audio.model")
    # 预测模型
    predicted = predicted_clf.predict(features)

    # 输出预测正确样本的平均值
    print(np.mean(predicted == labels))

    # 输出模型评估情况
    print(metrics.classification_report(features, predicted,
                                        target_names=labels))

    # 输出混淆矩阵
    print(metrics.confusion_matrix(labels, predicted))


def Fusion_model():
    features, labels = load_csv_data('/home/master/dataset/audio_wav/featureset.csv')

    print('多特征融合的音乐情感分类器 : \r')
    predicted_clf = joblib.load("music_fusion.model")
    # 预测模型
    predicted = predicted_clf.predict(features)

    # 输出预测正确样本的平均值
    print(np.mean(predicted == labels))

    # 输出模型评估情况
    print(metrics.classification_report(features, predicted,
                                        target_names=labels))

    # 输出混淆矩阵
    print(metrics.confusion_matrix(labels, predicted))
if __name__ == '__main__':

    #基于歌词
    Lyric_model()
    #基于音频
    Audio_model()
    #多特征融合
    Fusion_model()