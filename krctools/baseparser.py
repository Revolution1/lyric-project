# coding:utf-8

class parser:
    def __init__(self, rc):
        self._rc = rc
        self._dict = self.dictParse(self._rc)

    def getTag(self, tag):
        """
        :type tag : str
        :rtype : str
        """
        pass

    def getTagValue(self, tag):
        pass

    def getLyric(self):
        """
        :type tag : str
        :rtype: list
        """
        pass

    def getDict(self):
        """
        :type krc : str
        :rtype : dict
        """
        return self._dict

    @staticmethod
    def dictParse(xrc):
        """

        :type xrc: str
        :rtype dict:

        {
           'tag':{
               'ar':'the beatles',
               'ti':'I will'
           },
           'lyrics':[
               {
                   'lineTime':[0,0], # (start, duration)
                   'ly':[
                       [0,0,0,'words'],      # (start, duration, offset)
                   ]
               }
           ]
        }
        """
        pass