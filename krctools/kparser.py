# coding:utf-8
import re
from krctools.baseparser import parser


class KParser(parser):
    def __init__(self, krc):
        parser.__init__(self, krc)

    def getTag(self, tag):
        """
        :type tag : str
        :return: str
        """
        return '[%s:%s]' % (tag, self.getTagValue(tag))

    def getTagValue(self, tag):
        """
        :type tag : str
        :return: str
        """
        return self._dict['tag'].get(tag)

    def getLyric(self):
        """
        :type tag : str
        :rtype: list
        """
        return self._dict.get('lyrics')

    def getLyricN(self):
        return len(self.getLyric())

    @staticmethod
    def dictParse(krc):
        """
        :type krc : str
        :rtype : dict
        """
        krcDict = {}
        tagReg = r'\[(.*?):(.*?)\]'
        lyricReg = r'\[\d*,\d*\].+'
        lineTimeReg = r'\[(\d*),(\d*)\]'
        timeTagReg = r'<(\d+),(\d+),(\d+)>'
        t = re.findall(tagReg, krc)
        krcDict['tag'] = dict(t)
        t = re.findall(lyricReg, krc)
        krcDict['lyrics'] = []
        for i in t:
            l = {}
            lt = re.findall(lineTimeReg, i)[0]
            l['lineTime'] = [int(lt[0]), int(lt[1])]
            ll = re.split(timeTagReg, i)[1:]
            ly = []
            for j in range(0, len(ll), 4):
                ly.append([int(x) for x in ll[j:j + 3]] + [ll[j + 3].replace('\r', ''), ])
            l['ly'] = ly
            krcDict['lyrics'].append(l)
        return krcDict


if __name__ == '__main__':
    tests = """[id:$00000000]
[ar:the beatles]
[ti:Real Love]
[by:]
[hash:7e16491975b3431a56057ebbdf2041c0]
[al:]
[sign:]
[total:231836]
[offset:0]
[language:eyJjb250ZW50IjpbXSwidmVyc2lvbiI6MX0=]
[12014,5353]<0,350,0>All <350,301,0>my <651,300,0>little <951,649,0>plans <1600,551,0>and <2151,3202,0>schemes
[17367,5551]<0,350,0>Lost <350,399,0>like <749,251,0>some <1000,801,0>forgotten <1801,3750,0>dream"""
    from krctools.decode import Decoder

    f = '../cache/98104.krc'
    decoder = Decoder(fileName=f)
    tests = decoder.getDecoded()
    parser = KParser(tests)
    # print(parser.getTag('ti'))
    print(parser.getTag('ar'))
    print(parser.getTag('offset'))
    print(parser.getTagValue('ti'))
    print('LYRIC:\n', parser.getLyric())
    # print(parser.dictParse(tests))