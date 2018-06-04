# -*- coding:utf-8 -*-
# -------------------------------------------------- #
#     Be the change you want to see in the world.    #
#     Author：Sambo Qin                              #
#     Tel：1777-637-6617                             #
#     Mail：muse824@outlook.com                      #
# -------------------------------------------------- #
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV
from sklearn import metrics

def SVCClassifier_model(lyric_train,lyric_test):

    text_clf = Pipeline([('vect', CountVectorizer()),
                      ('tfidf', TfidfTransformer()),
                      ('clf', SGDClassifier(loss='hinge',
                                            penalty='l2',
                                            alpha=1e-3,
                                            n_iter=5,
                                            random_state=42)),
    ])

    text_clf = text_clf.fit(lyric_train.data, lyric_train.target)

    predicted = text_clf.predict(lyric_test.data)

    #输出预测正确样本的平均值
    print(np.mean(predicted == lyric_test.target))

    #输出模型评估情况
    print(metrics.classification_report(lyric_test.target, predicted,
        target_names=lyric_test.target_names))

    #输出混淆矩阵
    print(metrics.confusion_matrix(lyric_test.target, predicted))

    Best_model(text_clf,lyric_train)

    return


def Best_model(text_clf,lyric_train):

    parameters = {
        'vect__ngram_range': [(1, 1), (1, 2)],
               'tfidf__use_idf': (True, False),
               'clf__alpha': (1e-2, 1e-3),
    }
    '''
    parameters = {'C': [0.001, 0.003, 0.006, 0.009, 0.01, 0.04, 0.08, 0.1],
                  'kernel': ('linear', 'rbf',),
                  'gamma': [0.001, 0.005, 0.1, 0.15, 0.20, 0.23, 0.27],
                  'decision_function_shape': ['ovo', 'ovr'],
                  'class_weight': [{1: 7, 2: 1.83, 3: 3.17}],
                  }'''

    gs_clf = GridSearchCV(text_clf, parameters, n_jobs=-1)

    gs_clf = gs_clf.fit(lyric_train.data, lyric_train.target)

    best_parameters, score, _ = max(gs_clf.grid_scores_, key=lambda x: x[1])

    for param_name in sorted(parameters.keys()):
        print("%s: %r" % (param_name, best_parameters[param_name]))

    print(score)

if __name__ == '__main__':
    categories = ['happy', 'lonely',
                  'sad', 'sweet', 'quiet',"vent","strive","cure","miss"]
    # 从硬盘获取训练数据# 从硬盘获取训练数据
    lyric_train = load_files('/home/master/dataset/audio_lyric',
                             categories=categories,
                             load_content=True,
                             encoding='utf-8',
                             decode_error='strict',
                             shuffle=True, random_state=42)
    # 从硬盘获取训练数据# 从硬盘获取训练数据
    lyric_test = load_files('/home/master/dataset/lyric_test',
                            categories=categories,
                            load_content=True,
                            encoding='utf-8',
                            decode_error='strict',
                            shuffle=True, random_state=42)

    SVCClassifier_model(lyric_train,lyric_test)

