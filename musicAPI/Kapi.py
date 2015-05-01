# coding:utf-8
import requests

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0'}


def searchSong(songName):
    # {
    # "status": 1,
    #     "data": {
    #         "total": 3,
    #         "songs": [
    #             {
    #                 "singername": "The Beatles",
    #                 "songname": "I Will",
    #                 "filename": "the beatles - i will",
    #                 "hash": "871FAB69C6D5BB8C006AC44E02771F46",
    #                 "filesize": 1667366,
    #                 "bitrate": 128,
    #                 "timelength": 104000,
    #                 "extname": "mp3",
    #                 "ownercount": 779
    #             },
    #http://lib9.service.kugou.com/websearch/index.php?page=1&keyword={{songName}}&cmd=100
    url = 'http://lib9.service.kugou.com/websearch/index.php'
    gets = dict(page='1', keyword=songName, cmd='100')
    r = requests.get(url, params=gets, headers=header)
    r.raise_for_status()
    total=int(r.json()['data']['total'])
    if total>1:
        return r.json()['data']['songs']
    elif total==1:
        return [r.json()['data']['songs'],]
    elif total==0 :
        raise Exception('Get 0 searching result!')


def getSongUrl(hash):
    # http://m.kugou.com/app/i/getSongInfo.php?hash={{ hash }}&cmd=playInfo
    #{
    #     "fileName": "汪峰 - 在春天",
    #     "url": "http://fs.open.kugou.com/0e651975298dd3d82b556fdee0725648/55350c08/G007/M03/1E/1D/p4YBAFS20O-ASAOTABH0j04kMF8481.m4a",
    #     "fileSize": 1176719,
    #     "status": 1,
    #     "extName": "m4a",
    #     "bitRate": 33572,
    #     "timeLength": 280,
    #     "singerHead": "",
    #     "hash": "2b616f6ab9f8655210fd823b900085cc"
    # }
    url = 'http://m.kugou.com/app/i/getSongInfo.php'
    gets = {'hash': hash,
            'cmd': 'playInfo'}
    r = requests.get(url, params=gets, headers=header)
    r.raise_for_status()
    return r.json()['url']


def getkrc(filename, timelength, hash):
    # http://mobilecdn.kugou.com/new/app/i/krc.php?keyword={{filename}}&timelength={{timelength}}&type=1&cmd=200&hash={{hash}}
    url = 'http://mobilecdn.kugou.com/new/app/i/krc.php'
    gets = {'keyword': filename,
            'timelength': timelength,
            'type': '1',
            'cmd': '200',
            'hash': hash}
    r = requests.get(url, params=gets, headers=header)
    r.raise_for_status()
    return r.content


def getkrcByDict(song):
    return getkrc(song['filename'], song['timelength'], song['hash'])


if __name__ == '__main__':
    # print(getkrc('the beatles - i will', '225000', '871FAB69C6D5BB8C006AC44E02771F46'))
    # print(getSongUrl('871FAB69C6D5BB8C006AC44E02771F46'))
    # for i in searchSong('Drama, Love & \'Lationships'):
    #    print(i)
	print(getkrc('Drama, Love & \'Lationships','236000','5F7A5A959D0D6909B416569B269C3B7B'))