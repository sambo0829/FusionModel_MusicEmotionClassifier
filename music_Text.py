# -*- coding:utf-8 -*-
# -------------------------------------------------- #
#     Be the change you want to see in the world.    #
#     Author：Sambo Qin                              #
#     Tel：1777-637-6617                             #
#     Mail：muse824@outlook.com                      #
# -------------------------------------------------- #

import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')

import pymongo
#建立数据库以及表的连接
client = pymongo.MongoClient('localhost',27017)
music = client.musicInfo
#happy/sad/sweet/miss/quiet/lonely/cure/vent/strive
tag = "vent"
music_detail = music.s_detail_vent
music_lyric = music.s_lyric_vent

def Lyricdetail(data):
        # 接下来可实现提取想要的字段内的数据
        for item in data:
            if item.has_key('lyric') and item['lyric']:
                lyric = item['lyric']
                songid = item['songid']
                songname = item['songname']
                #print(lyric)
                localfile = "/home/master/dataset/audio_lyric/test/"+tag+"/{0}-{1}.txt".format(songname,songid)
                print(localfile)
                with open(localfile,"wb") as f:
                    f.write(bytes(lyric).decode("utf-8"))
                    music_lyric.insert_one(item)

if __name__ == '__main__':

    data = music_detail.find({"tags":re.compile('国语')},{'_id':0}).skip(1000).limit(500)
    Lyricdetail(data)

