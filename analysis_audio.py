# -*- coding:utf-8 -*-
# -------------------------------------------------- #
#     Be the change you want to see in the world.    #
#     Author：Sambo Qin                              #
#     Tel：1777-637-6617                             #
#     Mail：muse824@outlook.com                      #
# -------------------------------------------------- #
import time

import numpy as np
from sklearn import svm
import pandas as pd
from sklearn.externals import joblib
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split

#音频特征：mfcc,lpc,zcr,energy,sf,sr,loudness
feature_names = [
    ['mfccMean',"13"],['mfccVar',"13"],['mfccMax',"13"],['mfccMed',"13"],
    ['loudnessMean', "24"], ['loudnessVar', "24"],
    ['lpcMean',"3"],['lpcVar',"3"],['lpcMed',"3"],
    ['zcrMax', "1"],['zcrMean',"1"],['zcrVar',"1"], ['zcrMed', "1"],
    ['energyMax', "1"],['energyVar',"1"],['energyMed',"1"],
    ['srVar',"1"],['srMed',"1"],
    ['sfVar',"1"],['sfMed',"1"],
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

def bestSVM(features,labels):

    line_sp = []
    for i in range(len(labels)):
        line_sp.append(int(labels[i]))
    print(line_sp)

    svr = svm.SVC()
    parameters = {'C': [0.001, 0.003, 0.006, 0.009, 0.01, 0.04, 0.08, 0.1],
                  'kernel': ('linear', 'rbf',),
                  'gamma': [0.001, 0.005, 0.1, 0.15, 0.20, 0.23, 0.27],
                  'decision_function_shape': ['ovo', 'ovr'],
                  'class_weight': [{1: 7, 2: 1.83, 3: 3.17}],
                  }

    X_train, X_test, y_train, y_test = train_test_split(features, line_sp, test_size=.3, random_state=1)
    # GridSearchCV，sklearn的自动调优函数
    clf = GridSearchCV(svr, parameters,return_train_score = True)
    clf= clf.fit(X_train, y_train)

    # 保存模型
    joblib.dump(clf,"music.model")
    # 加载模型
    clf = joblib.load("music.model")

    # 使用a储存调优后的参数结果
    a = pd.DataFrame(clf.cv_results_)

    # 按照mean_test_score降序排列
    a.sort_values(['mean_test_score'], ascending=False)

    print(accuracy())
    # 输出最好的分类器参数，以及测试集的平均分类正确率
    print (clf.best_estimator_, clf.best_score_)

if __name__ == '__main__':
    start_time = time.time()
    features, labels = load_csv_data('/home/master/dataset/audio_wav/featureset.csv')
    print(features.shape[0])

    print('BestSVM: \r')
    bestSVM(features, labels)
    end_time = time.time()
    print(end_time-start_time)