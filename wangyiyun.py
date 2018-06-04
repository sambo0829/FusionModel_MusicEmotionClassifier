# -*- coding:utf-8 -*-
# -------------------------------------------------- #
#     Be the change you want to see in the world.    #
#     Author：Sambo Qin                              #
#     Tel：1777-637-6617                             #
#     Mail：muse824@outlook.com                      #
# -------------------------------------------------- #
import requests
from bs4 import BeautifulSoup
import json
import re

def get_html(url):
    header = {
        'User-Agent' : '',
        'Referer' : 'http://music.163.com',
        'Host' : 'music.163.com'
    }
