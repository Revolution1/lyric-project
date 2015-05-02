# coding:utf-8
# http://music.qq.com/miniportal/static/lyric/歌曲id求余100/歌曲id.xml
# http://stream1歌曲信息中的location值.qqmusic.qq.com/3歌曲ID（7位数，不足在前面补0）. mp3
# 例如之前搜索出来的第一首歌的地址应该是:
# http://stream18.qqmusic.qq.com/31679711. mp3
# 第二首歌的地址应该是
# http://stream13.qqmusic.qq.com/31516144. mp3
# ★搜索音乐（歌词）
# http://shopcgi.qqmusic.qq.com/fcgi-bin/shopsearch.fcg
# ?value=歌曲名&artist=歌手名&type=qry_song&out=json&page_no=页码&page_record_num=单页记录数量 #GB2312

# 就会得到这样的不标准json，之后的步骤简单的就说下，截取searchCallBack()中间的内容，对key进行加引号，然后就可以用json解码框架来解码
# 复制代码
# searchCallBack({result: "0", msg: "", totalnum: "138", curnum: "3", search: "记得", songlist: [
#     {idx: "1", song_id: "1679711", song_name: "记得", album_name: "上海老歌 CD07", singer_name: "欧阳飞莺(Chu Shia)",
#      location: "8", singer_id: "16343", album_id: "133528", price: "250"},
#     {idx: "2", song_id: "1516144", song_name: "记得", album_name: "小精选", singer_name: "刘浩龙", location: "3",
#      singer_id: "4797", album_id: "122193", price: "250"},
#     {idx: "3", song_id: "1512932", song_name: "记得（《爱情睡醒了》插曲）", album_name: "爱情睡醒了",
#      singer_name: "林俊杰", location: "8",
#      singer_id: "4286", album_id: "121988", price: "320"}]})
import re

import requests


header = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0'}
TIMEOUT = 3


def getLrc(id):
    url = 'http://music.qq.com/miniportal/static/lyric/%s/%s.xml' % (id[-2:], id)
    r = requests.get(url, headers=header, timeout=TIMEOUT)
    r.raise_for_status()
    return parseQ(r.text)


def parseQ(s):
    regx = r'<!\[CDATA\[(.*)\]\]>'
    lyric = re.findall(regx, s, re.DOTALL)[0]
    return lyric

def getMp3Url(id):
    pass


if __name__ == '__main__':
    print(getLrc('718475'))  # 发如雪
