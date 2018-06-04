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

#----------------------------------#
#                                  #
#       基于歌词的音乐情感分类器        #
#                                  #
#----------------------------------#
def SVMClassifier_lyric(lyric_train,lyric_test):

    #流水线处理
    text_clf = Pipeline([('vect', CountVectorizer()),
                      ('tfidf', TfidfTransformer()),
                      ('clf', svm.SVC()),
    ])

    text_clf = text_clf.fit(lyric_train.data, lyric_train.target)

    # 保存模型
    joblib.dump(text_clf,"music_lyric.model")
    # 加载模型
    predicted_clf = joblib.load("music_lyric.model")

    #预测模型
    predicted = predicted_clf.predict(lyric_test.data)

    #输出预测正确样本的平均值
    print(np.mean(predicted == lyric_test.target))

    #输出模型评估情况
    print(metrics.classification_report(lyric_test.target, predicted,
        target_names=lyric_test.target_names))

    #输出混淆矩阵
    print(metrics.confusion_matrix(lyric_test.target, predicted))

    #模型调优
    Best_lyricmodel(text_clf,lyric_train)

    return


def Best_lyricmodel(text_clf,lyric_train):

    parameters = {
                'vect__ngram_range': [(1, 1), (1, 2)],
                'tfidf__use_idf': (True, False),
    }

    gs_clf = GridSearchCV(text_clf, parameters, n_jobs=-1)

    gs_clf = gs_clf.fit(lyric_train.data, lyric_train.target)

    best_parameters, score, _ = max(gs_clf.grid_scores_, key=lambda x: x[1])

    for param_name in sorted(parameters.keys()):
        print("%s: %r" % (param_name, best_parameters[param_name]))

    print(score)

def Lyric_model():

    #标签分类
    categories = ['happy', 'lonely',
                  'sad', 'sweet', 'quiet',"vent","strive","cure","miss"]
    # 从硬盘获取训练数据# 从硬盘获取训练数据
    lyric_train = load_files('/home/master/dataset/audio_lyric',
                             categories=categories,
                             load_content=True,
                             encoding='utf-8',
                             decode_error='strict',
                             shuffle=True, random_state=42)
    # 从硬盘获取训练数据# 从硬盘获取测试数据
    lyric_test = load_files('/home/master/dataset/lyric_test',
                            categories=categories,
                            load_content=True,
                            encoding='utf-8',
                            decode_error='strict',
                            shuffle=True, random_state=42)
    #训练模型
    print('基于歌词的音乐情感分类器 : \r')
    SVMClassifier_lyric(lyric_train,lyric_test)

#----------------------------------#
#                                  #
#       基于音频的音乐情感分类器        #
#                                  #
#----------------------------------#

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

def SVMClassifier_audio(features,labels):

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
    #划分数据集
    X_train, X_test, y_train, y_test = train_test_split(features, line_sp, test_size=.3, random_state=1)

    # GridSearchCV，sklearn的自动调优函数
    clf = GridSearchCV(svr, parameters,return_train_score = True)
    clf= clf.fit(X_train, y_train)

    # 保存模型
    joblib.dump(clf,"music_audio.model")
    # 加载模型
    clf = joblib.load("music_audio.model")

    # 使用a储存调优后的参数结果
    a = pd.DataFrame(clf.cv_results_)

    # 按照mean_test_score降序排列
    a.sort_values(['mean_test_score'], ascending=False)

    print(accuracy())
    # 输出最好的分类器参数，以及测试集的平均分类正确率
    print (clf.best_estimator_, clf.best_score_)

def Audio_model():

    features, labels = load_csv_data('/home/master/dataset/audiofeature.csv')

    print('基于音频的音乐情感分类器 : \r')
    SVMClassifier_audio(features, labels)

#----------------------------------#
#                                  #
#       多特征融合的音乐情感分类器      #
#                                  #
#----------------------------------#

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

def SVMClassifier_fusion(features, labels):

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
    # 划分数据集
    X_train, X_test, y_train, y_test = train_test_split(features, line_sp, test_size=.3, random_state=1)

    # GridSearchCV，sklearn的自动调优函数
    clf = GridSearchCV(svr, parameters, return_train_score=True)
    clf = clf.fit(X_train, y_train)

    # 保存模型
    joblib.dump(clf, "music_fusion.model")
    # 加载模型
    clf = joblib.load("music_fusion.model")

    # 使用a储存调优后的参数结果
    a = pd.DataFrame(clf.cv_results_)

    # 按照mean_test_score降序排列
    a.sort_values(['mean_test_score'], ascending=False)

    print(accuracy())
    # 输出最好的分类器参数，以及测试集的平均分类正确率
    print (clf.best_estimator_, clf.best_score_)

def Fusion_model():
    features, labels = load_csv_data('/home/master/dataset/fusionfeature.csv')
    print('多特征融合的音乐情感分类器 : \r')
    SVMClassifier_fusion(features, labels)

if __name__ == '__main__':

    #基于歌词
    Lyric_model()
    #基于音频
    Audio_model()
    #多特征融合
    Fusion_model()