# coding:utf-8
# coding:utf-8
import re

from krctools.baseparser import parser


class QParser(parser):
    def getTag(self, tag):
        """
        :type tag : str
        :return: str
        """
        return '[%s:%s]' % (tag, self.getTagValue(tag))

    def getTagValue(self, tag):
        """
        :type tag : str
        :return: strm
        """
        return self._dict['tag'].get(tag)

    def getLyric(self):
        """
        :rtype: list
        """
        return self._dict.get('lyrics')

    def getLyricN(self):
        return len(self.getLyric())

    @staticmethod
    def dictParse(qrc):
        """
        :type qrc : str
        :rtype : dict
        """
        qrcDict = {}
        contentReg = r'Content="(.*)"/>'
        tagReg = r'\[(.*?):(.*?)\]'
        lyricReg = r'\[\d*,\d*\].+'
        lineTimeReg = r'\[(\d*),(\d*)\]'
        timeTagReg = r'\((\d+),(\d+)\)'
        qrc = re.findall(contentReg, qrc, re.DOTALL)[0]
        t = re.findall(tagReg, qrc)
        qrcDict['tag'] = dict(t)
        t = re.findall(lyricReg, qrc)
        qrcDict['lyrics'] = []
        for i in t:
            l = {}
            se = re.search(lineTimeReg, i)
            lt = se.groups()
            l['lineTime'] = [int(lt[0]), int(lt[1])]
            ll = re.split(timeTagReg, i[se.end():])
            # print(ll)
            ly = []
            for j in range(0, len(ll), 3):
                ly.append([ll[j], ] + [int(x) for x in ll[j + 1:j + 3]])
            l['ly'] = ly
            qrcDict['lyrics'].append(l)
        return qrcDict


if __name__ == '__main__':
    with open('../test/4581904.qrc', 'r') as f:
        tests = f.read()
        # print(tests)
        parser = QParser(tests)
        print(parser.getDict())
        # # print(parser.getTag('ti'))
        # print(parser.getTag('ar'))
        # print(parser.getTag('offset'))
        # print(parser.getTagValue('ti'))
        # print('LYRIC:\n', parser.getLyric())
        # print(parser.dictParse(tests))