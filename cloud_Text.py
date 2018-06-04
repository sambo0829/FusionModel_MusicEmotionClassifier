# -*- coding:utf-8 -*-
# -------------------------------------------------- #
#     Be the change you want to see in the world.    #
#     Author：Sambo Qin                              #
#     Tel：1777-637-6617                             #
#     Mail：muse824@outlook.com                      #
# -------------------------------------------------- #
import os
from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba

def chinesecloud():
    tag = "quiet"
    d = path.dirname(__file__)
    # 获取目标文件夹的路径
    filedir = "/home/master/dataset/audio_lyric/"+tag+"/"
    # 获取当前文件夹中的文件名称列表
    filenames = os.listdir(filedir)
    # 打开当前目录下的result.txt文件，如果没有则创建
    f = open("/home/master/dataset/"+tag+".txt", 'w')
    # 先遍历文件名
    for filename in filenames:
        filepath = filedir + '/' + filename
        # 遍历单个文件，读取行数
        for line in open(filepath):
            f.writelines(line)
            f.write('\n')
    # 关闭文件
    f.close()
    STOPWORDS = {"ti","offset0","by","al","ar",u"编曲",u"我们",u"一个",u"自己",u"没有",u"什么"}
    text = open(("/home/master/dataset/"+tag+".txt"), "rb").read()
    mytext = " ".join(jieba.cut(text))
    alice_mask = np.array(Image.open(path.join(d,"/home/master/dataset/image/"+tag+".png")))
    wc = WordCloud(font_path="/home/master/dataset/image/simkai.ttf", background_color="white",
                   max_words=1024, stopwords=STOPWORDS,mask=alice_mask)

    wc.generate(mytext)

    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.figure()
    plt.show()
    wc.to_file("/home/master/dataset/image/cloud_"+tag+".png")

if __name__ == '__main__':
    chinesecloud()
