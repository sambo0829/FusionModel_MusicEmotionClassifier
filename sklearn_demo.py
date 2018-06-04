# -*- coding:utf-8 -*-
# -------------------------------------------------- #
#     Be the change you want to see in the world.    #
#     Author：Sambo Qin                              #
#     Tel：1777-637-6617                             #
#     Mail：muse824@outlook.com                      #
# -------------------------------------------------- #
import pandas as pd


def dataclean():
    file = pd.read_csv("/home/master/dataset/audio_lyric/sad.csv",header=None)

    file["labels"] = "2"
    print(file).tail()
    file.to_csv("/home/master/dataset/audio_lyric/newfeel.csv",index=False,header=False,sep=",",mode="a+")

def dataclean2():
    print("123")


import numpy as np
from sklearn.cross_validation import KFold
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

feature_names = [
    'mfccMean','mfccVar','mfccMax',
    'lpcMean','lpcVar',
    'zcrMean','zcrVar',
    'energyMean','energyVar',
    'srMean','srVar',
    'sfMean','sfVar',
    'sdMean','sdVar',
    'ssMean','ssVar',
    'sssMean','sssVar',
    'pshMean','pshVar',
]

COLOUR_FIGURE = False


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


# ------------------------------------------------------------------------------
# 逻辑回归
# ------------------------------------------------------------------------------
def testLogistic(features, labels):
    kf = KFold(len(features), n_folds=9, shuffle=True)
    clf = LogisticRegression()
    result_set = [(clf.fit(features[train], labels[train]).predict(features[test]), test) for train, test in kf]
    score = [accuracy(labels[result[1]], result[0]) for result in result_set]
    print(score)


# ------------------------------------------------------------------------------
# 朴素贝叶斯
# ------------------------------------------------------------------------------
def testNaiveBayes(features, labels):
    kf = KFold(len(features), n_folds=9, shuffle=True)
    clf = GaussianNB()
    result_set = [(clf.fit(features[train], labels[train]).predict(features[test]), test) for train, test in kf]
    score = [accuracy(labels[result[1]], result[0]) for result in result_set]
    print(score)


# ------------------------------------------------------------------------------
# --- 支持向量机
# ------------------------------------------------------------------------------
def testSVM(features, labels):
    kf = KFold(len(features), n_folds=9, shuffle=True)
    clf = svm.SVC()
    result_set = [(clf.fit(features[train], labels[train]).predict(features[test]), test) for train, test in kf]
    score = [accuracy(labels[result[1]], result[0]) for result in result_set]
    print(score)


# ------------------------------------------------------------------------------
# --- 随机森林
# ------------------------------------------------------------------------------
def testRandomForest(features, labels):
    kf = KFold(len(features), n_folds=9, shuffle=True)
    clf = RandomForestClassifier()
    result_set = [(clf.fit(features[train], labels[train]).predict(features[test]), test) for train, test in kf]
    score = [accuracy(labels[result[1]], result[0]) for result in result_set]
    print(score)

if __name__ == '__main__':
    features, labels = load_csv_data('/home/master/dataset/audio_wav/featureset.csv')
    print(features)

    print('SVM: \r')
    testSVM(features, labels)

    print('GaussianNB: \r')
    testNaiveBayes(features, labels)

    print('LogisticRegression: \r')
    testLogistic(features, labels)

    print('Random Forest: \r')
    testRandomForest(features, labels)
