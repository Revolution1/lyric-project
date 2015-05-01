# coding:utf-8
import threading
import csv
import datetime


class Logger():
    def __init__(self, logFile='./log.txt'):
        self._LOG = []
        self._logToPrint = datetime.datetime.now().strftime("%Y-%m-%d %A %H:%M:%S")
        self._logToPrint = ''
        self.lock = threading.Lock()
        self._logFile = logFile

    def log(self, logInfo):
        self._LOG.append(logInfo)
        l = 'ID:%s\t%s\t%s' % (logInfo['ID'], logInfo['ti'], logInfo['OK'])
        self.logPrint(l)

    def logPrint(self, s):
        self._logToPrint += s+'\n'
        print(s)

    def logToDisk(self):
        self._logToPrint+='\n\n'
        with open(self._logFile, 'wb+') as f:
            f.write(self._logToPrint.encode())

    def logCsv(self, targetDir, csvName='qrcList.csv'):
        if targetDir.endswith('/'):
            targetDir = targetDir[:-1]
        # fieldNames=self._LOG[0].keys()s
        fieldNames = ['ID', 'ti', 'al', 'ar', 'OK']
        # fields = ['ID', '曲名', '专辑', '歌手', '处理结果']
        with open('%s/%s' % (targetDir, csvName), 'w') as f:
            writer = csv.DictWriter(f, fieldNames, lineterminator='\n')
            # writer.writerow(fieldNames)
            writer.writeheader()
            writer.writerows(self._LOG)


if __name__ == '__main__':
    logger = Logger()
    logger.logPrint('Test Log')
    logger.logPrint('Test Log2')
    logger.log({'ID': '123456', 'ti': '哈哈,哈"\'`', 'OK': 'OK'})
    logger.log({'ID': '12326', 'ti': 'sada', 'OK': 'fail to load'})
    logger.logCsv('d:/temp')
    # from pprint import pprint
    print(logger._LOG)
    print(logger._logToPrint)