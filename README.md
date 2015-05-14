#lyric project
 
一个多线程的将krc转换为qrc的工具,使用python3运行
 
目录结构:
 
 
    +-krctools/         处理krc文件的工具集
    |    decode.py         加密过的krc解码
    |    kparser.py        解析krc
    |    qparser.py        解析qrc
    |    k2q.py            将krc转换为qrc
    +-lpedit/           基于Qt的歌词编辑器 [未完成]
    +-mission/          歌曲列表
    +-musicAPI/         酷狗和QQ音乐的简易api
    +-test/             单元测试  [未完成]
    generate.py         主程序，多线程生成krc，提供标准命令行界面
    lplogger.py         一个线程安全的logger
 
 
#使用
 
    $ pip3 install -r requirements.txt
    $ python3 generate.py -h