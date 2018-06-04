# -*- coding:utf-8 -*-
# -------------------------------------------------- #
#     Be the change you want to see in the world.    #
#     Author：Sambo Qin                              #
#     Tel：1777-637-6617                             #
#     Mail：muse824@outlook.com                      #
# -------------------------------------------------- #

import os
import subprocess

def audio_trans(filepath,new_path):

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

if __name__ == '__main__':

    filepath = "/home/master/dataset/audio_m4a/lonely/"  # 添加源文件路径
    new_path = "/home/master/dataset/audio_wav/lonely/"  # 输出路径
    audio_trans(filepath,new_path)
