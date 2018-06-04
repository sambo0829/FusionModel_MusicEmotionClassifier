# -*- coding:utf-8 -*-
# -------------------------------------------------- #
#     Be the change you want to see in the world.    #
#     Author：Sambo Qin                              #
#     Tel：1777-637-6617                             #
#     Mail：muse824@outlook.com                      #
# -------------------------------------------------- #
import datetime
import re
import requests
import urllib
import json
import pymongo
from multiprocessing import Pool

#建立数据库以及表的连接
client = pymongo.MongoClient('localhost',27017,connect=False)
#happy/sad/sweet/miss/quiet/lonely/cure/vent/strive
music = client.musicInfo
localtag = "sweet"
s_list_song = music.s_detail_sweet
music_down = music.s_audio_sweet

def getVkey(songmid):

    vkey_url = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?g_tk=5381&loginUin=0&' \
               'hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&' \
               'cid=205361747&uin=0&' \
               'songmid={0}&filename=C400{1}.m4a&guid=9407604343'.format(songmid,songmid)
    html = requests.get(vkey_url).text
    js = json.loads(html)
    vkey = js['data']['items'][0]['vkey']
    return vkey

def MusicDownload(item):

    if 'songmid' in item:
        Vkey = getVkey(item['songmid'])
        songid = item['songid']
        songmid = item['songmid']
        songname = item['songname']
        try:
            music_url = 'http://dl.stream.qqmusic.qq.com/C400{0}.m4a?vkey={1}&guid=9407604343&uin=0&fromtag=66'.format(songmid, Vkey)
            localpath = u'/home/master/dataset/audio_m4a/' + localtag + '/{0}-{1}.m4a'.format(songname, songid)
            urllib.urlretrieve(music_url,localpath)
            music_down.insert_one(item)

        except:
            print('Download Wrong！')
    else:
        print ('......')
    return

if __name__ == '__main__':

    # 开启N个进程爬取
    pool = Pool(4)
    # 为了防止爬取中途停止，设置记录数
    count = 0
    # 以每次40个的数量从数据表拿出来
    number = 20
    while True:
        try:
            data = s_list_song.find({'tags':re.compile('国语')},{'_id':0}).skip(count).limit(number)
            pool.map(MusicDownload,data)
            count = count + number
            print (music_down.count())
            if music_down.count() > 100:
                break
            print(datetime.datetime.now())
        except:
            continue

