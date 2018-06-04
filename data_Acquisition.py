# -*- coding:utf-8 -*-
# -------------------------------------------------- #
#     Be the change you want to see in the world.    #
#     Author: Sambo Qin                              #
#     Tel: 1777-637-6617                             #
#     Mail: muse824@outlook.com                      #
# -------------------------------------------------- #

import datetime
import sys
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')
import re
import json
import requests
import urllib
import pandas as pd
from multiprocessing import Pool

import pymongo
#连接mongo服务器
client = pymongo.MongoClient('localhost',27017,connect=False)
#happy 117/sad 52/sweet 59/miss 68/quiet 122/lonely 55/cure 116/vent 126/strive 125
music = client.musicdata
localtag = "lonely"
music_list = music.s_list_lonely
music_detail = music.s_detail_lonely
music_lyric = music.s_lyric_lonely
music_audio = music.s_audio_lonely

#----------------------------------#
#                                  #
#       爬取歌单内歌曲信息             #
#                                  #
#----------------------------------#

#爬取歌单id
def getDissid(sin,ein):
    url = 'https://c.y.qq.com/splcloud/fcgi-bin/fcg_get_diss_by_tag.fcg'
    header = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'cookie':'RK=7dNm4/X+Yj; tvfe_boss_uuid=bf00ee54e9081ab4; pgv_pvi=8772238336; pac_uid=1_857193777; pgv_pvid=6457341280; o_cookie=80; ptcz=c761e59c8c8d6bd5198866d02a5cb7313af1af468006c455d6c2b5d26201d42e; pgv_si=s10759168; _qpsvr_localtk=0.08285763449905015; ptisp=ctc; luin=o0857193777; lskey=00010000228dd1371b945c68ecfd3b71d3071425024a7a8a2a23e3ffcb5b9904c9f7088d2ea8c01539ffed92; pt2gguin=o0857193777; uin=o0857193777; skey=@Kydi7w0EI; p_uin=o0857193777; p_skey=HjsE9sEjznJfXk*9KFEeW4VZr6i3*tlXZ2nuzEw8kCg_; pt4_token=c-p6sv3JEboA51cSQ3ABqxM8O80Jct3jYYkgy-aEQuE_; p_luin=o0857193777; p_lskey=000400008f9c296cd10c03a5173d22a184aad124d791568e90e4198beb8ad699a4d02fbfc059f71ab3d8758c; ts_last=y.qq.com/portal/playlist.html; ts_refer=ui.ptlogin2.qq.com/cgi-bin/login; ts_uid=3392060960',
        'referer':'https://y.qq.com/portal/playlist.html'
    }
    paramter = {
        'g_tk':'1089387893',
        'jsonpCallback':'getPlaylist',
        'loginUin':'0',
        'hostUin':'0',
        'format':'jsonp',
        'inCharset':'utf8',
        'outCharset':'utf-8',
        'notice':'0',
        'platform':'yqq',
        'needNewCode':'0',
        'categoryId':'55', #t1
        'sortId':'5', #t2
        'sin':sin,#开始结点
        'ein':ein #结束结点，用于翻页
    }
    html = requests.get(url=url,params=paramter,headers=header)
    res = json.loads(html.text.lstrip('getPlaylist(').rstrip(')'))['data']['list']
    data = []
    if res != []:
        for t_item in res:
            item = {}
            ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')#用于去掉非法字符
            item['createtime']      = t_item['createtime']
            item['creator_qq']      = t_item['creator']['qq']
            item['creator_name']    = t_item['creator']['name']
            item['creator_name'] = ILLEGAL_CHARACTERS_RE.sub(r'', item['creator_name'])
            item['creator_isVip']    = t_item['creator']['isVip']
            item['dissid']          = t_item['dissid'] #提取歌单id，用于后续提取歌曲id
            item['dissname']        = t_item['dissname'] #歌单名称
            item['dissname'] = ILLEGAL_CHARACTERS_RE.sub(r'', item['dissname'])
            item['listennum']       = t_item['listennum'] #播放量
            data.append(item)
    return data

#爬取歌曲id
def getSongid(dissid):
    url = 'https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg'
    header = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'cookie':'RK=7dNm4/X+Yj; tvfe_boss_uuid=bf00ee54e9081ab4; pgv_pvi=8772238336; pac_uid=1_857193777; pgv_pvid=6457341280; o_cookie=857193777; ptcz=c761e59c8c8d6bd5198866d02a5cb7313af1af468006c455d6c2b5d26201d42e; pgv_si=s10759168; _qpsvr_localtk=0.08285763449905015; ptisp=ctc; luin=o0857193777; lskey=00010000228dd1371b945c68ecfd3b71d3071425024a7a8a2a23e3ffcb5b9904c9f7088d2ea8c01539ffed92; pt2gguin=o0857193777; uin=o0857193777; skey=@Kydi7w0EI; p_uin=o0857193777; p_skey=HjsE9sEjznJfXk*9KFEeW4VZr6i3*tlXZ2nuzEw8kCg_; pt4_token=c-p6sv3JEboA51cSQ3ABqxM8O80Jct3jYYkgy-aEQuE_; p_luin=o0857193777; p_lskey=000400008f9c296cd10c03a5173d22a184aad124d791568e90e4198beb8ad699a4d02fbfc059f71ab3d8758c; ts_last=y.qq.com/portal/playlist.html; ts_refer=ui.ptlogin2.qq.com/cgi-bin/login; ts_uid=3392060960',
        'referer':'https://y.qq.com/n/yqq/playlist/{}.html'.format(dissid)
    }
    paramters = {
        'type':'1',
        'json':'1',
        'utf8':'1',
        'onlysong':'0',
        'disstid':dissid,
        'format':'jsonp',
        'g_tk':'1089387893',
        'jsonpCallback':'playlistinfoCallback',
        'loginUin':'857193777',
        'hostUin':'0',
        'inCharset':'utf8',
        'outCharset':'utf-8',
        'notice':0,
        'platform':'yqq',
        'needNewCode':0
    }
    html = requests.get(url=url,params=paramters,headers=header)
    cdlist = json.loads(html.text.lstrip('playlistinfoCallback(').rstrip(')'))['cdlist']
    if len(cdlist)>=1:
        cdlist = cdlist[0]

    data = []   #用于保存歌曲部分信息

    tags = ','.join([i['name'] for i in cdlist['tags']])
    for item in cdlist['songlist'] :
        tmp = {}
        tmp['albumname'] = item['albumname']
        tmp['songname']  = item['songname']
        tmp['singer']  = ','.join([i['name'] for i in item['singer']])
        if 'songmid' in item:
            tmp['songmid'] = item['songmid']
        if 'songid' in item:
            tmp['songid'] = item['songid']
        if tags.find(u"国语") != -1:
            tmp['tags'] = tags
            data.append(tmp)
    return data

def musicList():

    #爬取分类歌单信息
    sin = 0
    ein = sin+29
    s_list = []
    while True:
        print (sin)
        data = getDissid(sin,ein)
        s_list.extend(data)
        sin = sin + 30
        ein = sin + 29
        if ein > 824:
            break
    t_data = pd.DataFrame(s_list)
    print(t_data)

    dissids = t_data['dissid'].values

    for dissid in range(0,len(dissids)):
        print (dissid,dissids[dissid],)
        d1 = getSongid(str(dissids[dissid]))
        if d1 != []:
            music_list.insert_many(d1)
            print ('Song Insert successfully!',len(d1))
        else:
            print ('..........')

#----------------------------------#
#                                  #
#        爬取歌曲全部信息             #
#                                  #
#----------------------------------#

#获取歌词内容
def getLyric(musicid, songmid):
    url = 'https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric.fcg'
    header = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'referer':'https://y.qq.com/n/yqq/song/{}.html'.format(songmid)
    }
    paramters = {
        'nobase64':1,
        'musicid':musicid, #传入之前获取到的id
        'callback':'jsonp1',
        'g_tk':'1134533366',
        'jsonpCallback':'jsonp1',
        'loginUin':'0',
        'hostUin':'0',
        'format':'jsonp',
        'inCharset':'utf8',
        'outCharset':'utf-8',
        'notice':'0',
        'platform':'yqq',
        'needNewCode':'0'
    }
    html = requests.get(url=url,params=paramters,headers=header)
    res = json.loads(html.text.lstrip('jsonp1(').rstrip(')'))
    #由于一部分歌曲是没有上传歌词，因此没有默认为空
    if 'lyric' in res:
        lyric = json.loads(html.text.lstrip('jsonp1(').rstrip(')'))['lyric']
        #对歌词内容做稍微清洗
        dr1 = re.compile(r'&#\d.;',re.S)
        dr2 = re.compile(r'\[\d+\]',re.S)
        dd = dr1.sub(r'',lyric)
        dd = dr2.sub(r'\n',dd).replace('\n\n','\n')
        return dd
    else:
        return ""

#获取歌曲详细信息
def getDetail(songid,songmid):
    spp = ['c.y.qq.com','59.37.96.220','101.227.139.217','59.37.96.220','59.37.96.220']
    url = 'https://c.y.qq.com/v8/fcg-bin/fcg_play_single_song.fcg'
    sp = ['103.18.209.26','y.qq.com','103.18.209.25','106.38.181.141','180.153.105.167']
    header = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'referer':'https://y.qq.com/n/yqq/song/{}.html'.format(songid)
    }
    paramters = {
        'songmid':songmid,
        'tpl':'yqq_song_detail',
        'format':'jsonp',
        'callback':'getOneSongInfoCallback',
        'g_tk':'1134533366',
        'jsonpCallback':'getOneSongInfoCallback',
        'loginUin':'0',
        'hostUin':'0',
        'inCharset':'utf8',
        'outCharset':'utf-8',
        'notice':0,
        'platform':'yqq',
        'needNewCode':0
    }
    #html = requests.get(url=url,params=paramters,headers=header,proxies=getProxies("HOOF09GO4963E22D","7ED29B96EFC8AA19"))
    html = requests.get(url=url,params=paramters,headers=header,verify=True)
    detail = json.loads(html.text.lstrip('getOneSongInfoCallback(').rstrip(')'))['data']
    data = {}
    if len(detail)>0:
        detail = detail[0]
        data['subtitle'] = detail['subtitle']
        data['title'] = detail['title']
        data['time_public'] = detail['time_public']
        try:
            data['url'] = json.loads(html.text.lstrip('getOneSongInfoCallback(').rstrip(')'))['url'][str(songid)]
        except:
            data['url'] = ""
    return data

#爬取并且存入MongoDB数据库
def insertDetail(item):
    r1 = u'[’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
    if 'songmid' in item:
        lyric = getLyric(item['songid'],item['songmid']).encode('utf-8')
        s_detail = getDetail(item['songid'],item['songmid'])
        s_detail['lyric'] = lyric
        s_detail['singer'] = item['singer']
        s_detail['tags'] = item['tags']
        s_detail['albumname'] = item['albumname']
        s_detail['songname'] = re.sub(r1, '',item['songname'])
        s_detail['songmid'] = item['songmid']
        s_detail['songid'] = item['songid']
        music_detail.insert_one(s_detail)
        print ('Detail Insert successfully!')

    else:
        print ('++++++++++')

def musicDetail():
    #开启N个进程爬取
    pool  = Pool(4)
    # 为了防止爬取中途停止，设置记录数
    count = 0
    # 以每次20个的数量从数据表拿出来
    number = 20
    while True:
        try:
            data = music_list.find({'songname':re.compile("^\W+?$")},{'_id': 0}).skip(count).limit(number)
            pool.map(insertDetail,data)
            count = count + number
            if music_detail.count() > 2000:
                break
            print(datetime.datetime.now())
        except:
            continue

#----------------------------------#
#                                  #
#        下载歌词                    #
#                                  #
#----------------------------------#

def Lyricdetail(data):
    # 接下来可实现提取想要的字段内的数据
    for item in data:
        if item.has_key('lyric') and item['lyric']:
            lyric = item['lyric']
            songid = item['songid']
            songname = item['songname']
            # print(lyric)
            localfile = u"/home/master/dataset/audio_lyric/" + localtag + "/{0}-{1}.txt".format(songname, songid)
            print(localfile)
            with open(localfile, "wb") as f:
                f.write(bytes(lyric).decode("utf-8"))
                music_lyric.insert_one(item)

def musicText():
    data = music_detail.find({},{'_id': 0})
    Lyricdetail(data)

#----------------------------------#
#                                  #
#           下载音频                 #
#                                  #
#----------------------------------#
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
            music_audio.insert_one(item)

        except:
            print('Audio Download Wrong！')
    else:
        print ('**********')
    return

def musicAudio():

    # 开启N个进程爬取
    pool = Pool(4)
    # 为了防止爬取中途停止，设置记录数
    count = 0
    # 以每次20个的数量从数据表拿出来
    number = 20
    while True:
        try:
            data = music_detail.find({},{'_id':0}).skip(count).limit(number)
            pool.map(MusicDownload,data)
            count = count + number
            if music_audio.count() > 150:
                break
            print(datetime.datetime.now())
        except:
            continue

if __name__ == '__main__':

    #获取歌单内歌曲信息
    musicList()
    #获取歌曲详细信息
    musicDetail()
    #下载歌词
    musicText()
    #下载音频
    musicAudio()
