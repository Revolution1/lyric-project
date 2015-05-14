# coding:utf-8
import musicAPI
import krctools as kt
import mission
import queue
import threading
import os
from lpLogger import Logger
from datetime import datetime

TARGET_DIR = './qrc.output'
LIST_FILE = './mission/song-list.csv'
CACHE_DIR = './cache'
THREAD_COUNT = 5
exitFlag = 0
total = [0, 0, 0]  # Success Fail Total
__version__ = '0.1'


class GenQueue(queue.Queue):
    def __init__(self, maxsize=0):
        queue.Queue.__init__(self, maxsize)
        self.lock = threading.Lock()


class GenThread(threading.Thread):
    def __init__(self, name, queue, targetDir, logger, listLen):
        threading.Thread.__init__(self)
        self.targetDir = targetDir
        self.logger = logger
        self.name = name
        self.queue = queue
        self.listLen = listLen

    def run(self):
        while not exitFlag:
            self.queue.lock.acquire()
            if not self.queue.empty():
                songInfo = self.queue.get()
                self.queue.lock.release()
                process(songInfo, self.targetDir, self.logger, self.listLen)
            else:
                self.queue.lock.release()


def process(songInfo, targetDir, logger, listLen):
    global total
    flag = 0
    l = songInfo.copy()
    try:
        krcFile = '%s/%s.krc' % (CACHE_DIR, songInfo['ID'])
        if os.path.isfile(krcFile):
            with open(krcFile, 'rb') as f:
                krc = f.read()
        else:
            try:
                songs = musicAPI.searchSong(' '.join([songInfo['ti'], songInfo['ar']]))
            except:
                raise Exception('Fail searching')
            try:
                krc = musicAPI.getkrcByDict(songs[0])
            except:
                raise Exception('Fail downloading krc')
            try:
                with open(krcFile, 'wb') as f:
                    krc = f.write(krc)
            except:
                raise Exception('Fail caching')
        try:
            krc_decoded = kt.Decoder.decode(krc)
        except:
            raise Exception('Fail decoding krc')
        try:
            qrc = kt.k2q.convert(krc_decoded, tag=songInfo)
        except:
            raise Exception('Fail converting to qrc')
        with open('%s/%s.qrc' % (targetDir, songInfo['ID']), 'wb') as f:
            f.write(qrc.encode('utf-8'))
        l['OK'] = 'OK'
    except Exception as e:
        l['OK'] = e.args[0]
        flag = 1
    finally:
        logger.lock.acquire()
        logger.log(l)
        total[flag] += 1
        total[2] += 1
        if total[2] % 10 == 0:
            print('Progress: {0:.2f}%\t Count:{1}'.format(total[2] / listLen * 100, total[2]))
        logger.lock.release()


def generate(params):
    threadCount = int(params['count']) if params['count'] else THREAD_COUNT
    targetDir = params['targetDir'] if params['targetDir'] else TARGET_DIR
    listFile = params['listFile'] if params['listFile'] else LIST_FILE

    if not os.path.isdir(targetDir):
        os.mkdir(targetDir)
    songList = mission.getList(listFile)
    # songList = [mission.getList(listFile)[3],] #for debug
    global total
    logger = Logger()
    queue = GenQueue(len(songList))
    threads = []
    # Open thread pool
    for i in range(threadCount):
        thread = GenThread('thread-%d' % i, queue, targetDir, logger, len(songList))
        thread.start()
        threads.append(thread)
    # Fill the task queue
    queue.lock.acquire()
    startTime = datetime.now()
    for i in range(len(songList)):
        l = songList[i]
        queue.put(l)
    logger.logPrint('%s\nStart Generating with %s threads....' % (startTime.strftime('%Y-%m-%d %H:%M:%S'), threadCount))
    queue.lock.release()
    # Wait for threads to finish
    while not queue.empty():
        pass
    global exitFlag
    exitFlag = 1
    for t in threads:
        t.join()

    logger.logPrint('All Done!')
    logger.logPrint('Succeeded:%d   Failed:%d   Total:%d\n' % tuple(total))
    delta = datetime.now() - startTime
    logger.logPrint('It takes %s seconds to finish.' % delta.seconds)
    logger.logCsv(targetDir)
    logger.logPrint('CSV dumped.')
    logger.logToDisk()


if __name__ == '__main__':
    optstr = """
    Usage:
        generate.py [-n <threadCount>] [-r <listFile>] [-t <targetDir>]
        generate.py -h | --help
        generate.py -v | --version

    Options:
        -h, --help                                  Show this screen.
        -v, --version                               Show version info.
        -n <threadCcount>, --count <threadCount>    How many threads to run,
                                                    default: 5 .
        -r <listFile>, --listFile <listFile>        The csv song-list.
                                                    default: './mission/song-list.csv'
        -t <targetDir>, --targetDir <targetDir>     Folder to put qrc files.
                                                    default: './qrc.output'
    """
    import sys
    from docopt import docopt

    opt = docopt(optstr, sys.argv[1:], version='Lyric-project %s with python3.4' % __version__)
    params = dict(
        count=opt['--count'],
        listFile=opt['--listFile'],
        targetDir=opt['--targetDir']
    )
    if not os.path.isdir(CACHE_DIR):
        os.mkdir(CACHE_DIR)
    generate(params)