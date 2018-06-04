# -*- coding:utf-8 -*-
# -------------------------------------------------- #
#     Be the change you want to see in the world.    #
#     Author：Sambo Qin                              #
#     Tel：1777-637-6617                             #
#     Mail：muse824@outlook.com                      #
# -------------------------------------------------- #
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from jieba import analyse
# 引入TF-IDF关键词抽取接口
tfidf = analyse.extract_tags
# 引入TextRank关键词抽取接口
textrank = analyse.textrank


def allkeyword():

    file_dir = "/home/master/dataset/audio_lyric/sweet/"
    filename = os.listdir(file_dir)
    filepath = []

    for i in range(len(filename)):
          filename[i] = file_dir+filename[i]
          filepath.append(filename[i])
    for i in range(len(filename)):
        localfile = open('/home/master/dataset/audio_lyric/sweet.csv','a+') # 设置newline，否则两行之间会空一行
        lyric = open(filename[i],"r+").read()

        # 基于TF-IDF算法进行关键词抽取
        keywords = tfidf(lyric)
        print "\nkeywords by tfidf:"
        # 输出抽取出的关键词
        for keyword in keywords:
             localfile.writelines(keyword+",")
        localfile.write("\n")

        print "\nkeywords by textrank:"
        # 基于TextRank算法进行关键词抽取
        keywords = textrank(lyric)
        # 输出抽取出的关键词
        for keyword in keywords:
             localfile.writelines(keyword+",")
        localfile.write("\n")
        localfile.close()


if __name__ == '__main__':
    allkeyword()


