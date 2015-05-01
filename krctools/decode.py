# coding:utf-8
import zlib

krc_keys = [64, 71, 97, 119, 94, 50, 116, 71, 81, 54, 49, 45, 206, 210, 110, 105]
# Key      {'@','G','a','w', '^','2','t','G','Q','6', '1','-','Î', 'ò', 'n', 'i' }

class Decoder:
    def __init__(self, data=None, fileName=None):
        self._load(data, fileName)

    @staticmethod
    def decode(data):
        """
            :rtype : str
        """
        # if not data.startswith(b'krc1'):
        # # header check
        # raise Exception('Not a krc file!')
        zd = bytes()
        for i in range(4, len(data)):
            zd += bytes([data[i] ^ krc_keys[(i - 4) % 16]])
        return zlib.decompress(zd).decode()[1:]


    def _load(self, data=None, fileName=None):
        if data:
            self._data = data
        elif fileName:
            f = open(fileName, 'rb')
            self._data = f.read()
            f.close()
        else:
            self._data = ''

    def getDecoded(self):
        return self.decode(self._data)


if __name__ == '__main__':
    # decoder = Decoder(fileName='../test/Lucy-In-The-Sky-With-Diamonds.krc')
    # print(decoder.getDecoded())
    # f='../test/Real-love.krc'
    f = '../cache/98104.krc'
    decoder = Decoder(fileName=f)
    print(decoder.getDecoded())