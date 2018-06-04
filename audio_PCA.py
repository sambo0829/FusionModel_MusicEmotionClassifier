# -*- coding:utf-8 -*-
# -------------------------------------------------- #
#     Be the change you want to see in the world.    #
#     Author：Sambo Qin                              #
#     Tel：1777-637-6617                             #
#     Mail：muse824@outlook.com                      #
# -------------------------------------------------- #
from sklearn.decomposition import PCA
import numpy as np
from sklearn.preprocessing import StandardScaler

def load_csv_data(filename):
    data = []
    datafile = open(filename)
    for line in datafile:
        fields = line.strip().split(',')
        data.append([float(field) for field in fields[:-1]])
    data = np.array(data)
    #print(data)
    X_scaler = StandardScaler()
    x = X_scaler.fit_transform(data)

    # PCA
    pca = PCA(n_components=0.95)  # 保证降维后的数据保持90%的信息
    pca.fit(x)
    print(pca.transform(x))

    return data

if __name__ == '__main__':
    features = load_csv_data('/home/master/dataset/audio_wav/allfeature.csv')

