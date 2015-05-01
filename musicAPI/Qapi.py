# coding:utf-8
# http://music.qq.com/miniportal/static/lyric/歌曲id求余100/歌曲id.xml
import requests
import re

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0'}

def getLrc(id):
    url='http://music.qq.com/miniportal/static/lyric/%s/%s.xml'%(id[-2:],id)
    r = requests.get(url, headers=header)
    r.raise_for_status()
    return parse(r.text)

def parseQ(s):
    regx=r'<!\[CDATA\[(.*)\]\]>'
    lyric=re.findall(regx,s,re.DOTALL)[0]
    return lyric


if __name__ == '__main__':
    print(getLrc('718475'))
