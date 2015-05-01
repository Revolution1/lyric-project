# coding:utf-8
import csv


def getList(listFile):
    with open(listFile, 'r') as f:
        # print(f.read(11))
        dicReader = csv.DictReader(f)
        # for i in dicReader:
        # print(i)
        return [i for i in dicReader]


if __name__ == '__main__':
    for i in getList('./song-list.csv')[:5]:
        print(i)