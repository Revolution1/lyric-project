# coding:utf-8
import time
import re
from krctools.kparser import KParser


class k2q:
    def __init__(self, krc, tag=None):
        self._krc = krc
        self._qrc = self.convert(self._krc, tag)

    @staticmethod
    def convert(krc, tag=None):
        timeStamp = int(time.time())
        newLine = '\r\n'
        head = newLine.join(['<?xml version="1.0" encoding="utf-8"?>',
                             '<QrcInfos>',
                             '<QrcHeadInfo SaveTime="%d" Version="100"/>' % timeStamp,
                             '<LyricInfo LyricCount="1">',
                             '<Lyric_1 LyricType="1" LyricContent="'])
        foot = newLine + '"/></LyricInfo></QrcInfos>'
        p = KParser(krc)
        # add tags
        tags = ['ti', 'ar', 'al', 'by', 'offset']
        content = ''
        if tag:
            for i in range(len(tags)):
                t = tags[i]
                if t == 'by':
                    content += '[by:]%s' % newLine
                    continue
                if t in tag:
                    content += '[%s:%s]%s' % (t, replaceApos(tag[t]), newLine)
                else:
                    try:
                        content += replaceApos(p.getTag(t)) + newLine
                    except:
                        pass
        qLyric = []
        firstLine = '%s - %s' % (tag['ti'], tag['ar'])
        for j in range(len(p.getLyric())):  # Per line
            i = p.getLyric()[j]
            lineStart = i['lineTime'][0]
            # lineDuration = i['lineTime'][1]
            if j == 0:
                fD = int(lineStart * 3 / 4)
                fS = int(lineStart / 5)
                qLyric.append('[%s,%s]%s(%s,%s)' % (fS, fD, firstLine, fS, fD))
            totalDuration = 0
            ly = ''
            for k in range(len(i['ly'])):  # Per word
                l = i['ly'][k]
                start, duration, offset, word = l
                start += lineStart
                nextStartTime = 9999999
                if k == len(i['ly']) - 1:
                    if j != len(p.getLyric()) - 1:
                        nextStartTime = p.getLyric()[j + 1]['lineTime'][0]
                elif k != len(i['ly']) - 1:
                    nextStartTime = i['ly'][k + 1][0] + lineStart
                word = replaceApos(word)
                word = doReplaces(word)
                if k == 0:
                    word = word.capitalize()
                if k == len(i['ly']) - 1:
                    word = replaceEndLinePunctuations(word)
                if start + duration >= nextStartTime:
                    duration = nextStartTime - start
                ly += '%s(%s,%s)' % (word, start, duration)
                totalDuration += duration
            # if totalDuration < lineDuration:  # TotalDuration should always less than lineDuration
            lineDuration = totalDuration
            ly = '[%s,%s]' % (lineStart, lineDuration) + ly
            qLyric.append(ly)
        content += newLine.join(qLyric)
        return head + content + foot

    def getQrc(self):
        return self.convert(self._krc)


def replaceApos(s):
    return s.replace('\'', '&apos;')


def doReplaces(s):
    d = {'[dD]ont': "don't",
         '[cC]ant': "can't",
         '[lL]ets': "let's",
         '\r': '',
         '[iI]ve': "I've",
         '"': '&quot;',
         '[iI]snt': "isn't",
         '[hH]adnt': "hadn't",
         '[sS]hant': "shan't",
         '[wW]ont': "won't",
         '[iI]m': "I'm",
         '[aA]int': "ain't",
         '[hH]asnt': "hasn't",
         '[hH]avent': "haven't",
         '[iI]ts': "it's"}
    for i in d:
        s = re.sub(r'\W?(%s)\W+|^%s$' % (i,i), d[i], s)
    s = re.sub(r"(?=[^a-zA-Z]?)(i)(?=[^a-zA-Z]+)|^i$", 'I', s)
    s = s.replace('\\','')
    return replaceApos(s)


def replaceEndLinePunctuations(s):
    pReg = r'[,.?!]*$'
    return re.sub(pReg, '', s)


if __name__ == '__main__':
    tests = '''[id:$00000000]
[ar:the beatles]
[ti:Real Love]
[by:]
[hash:7e16491975b3431a56057ebbdf2041c0]
[al:]
[sign:]
[total:231836]
[offset:0]
[language:eyJjb250ZW50IjpbXSwidmVyc2lvbiI6MX0=]
[12014,5353]lets <0,350,0>ive <350,301,0>i'm <651,900,0>Ive <951,649,0>plans <1600,551,0>and <2151,5500,0>schemes.
[17367,5551]<0,350,0>lost <350,399,0>like <749,251,0>some <1000,801,0>forgotten\\' <1801,3750,0>\\\\\dream'''
    # print(tests.splitlines()[10:])
    # print(k2q.replaceQuote('[17367,5551]<0,350,0>Lost <350,399,0>like <749,251,0>some <1000,801,0>forgotten <1801,3750,0>dream'))
    # converter=k2q(tests)
    # print(converter.getQrc())
    # print(doReplaces(tests))
    # print(capitalize(tests))
    # print(tests)
    # print(k2q.standardFilter(tests.splitlines()[10:], dict(ti='Real Love', ar='The Beatles', al='Anthology 2')))
    from krctools.decode import Decoder
    f='../cache/98104.krc'
    decoder = Decoder(fileName=f)
    tests = decoder.getDecoded()
    print(k2q.convert(tests, dict(ti='Real Love', ar='The Beatles')))
