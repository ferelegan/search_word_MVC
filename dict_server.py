"""
在线字典 服务端
"""

from multiprocessing import Process
from socket import *
from time import sleep

from dict_db import *

class SearchWordTCP:
    def __init__(self):
        self.__host = '0.0.0.0'
        self.__port = 8888
        self.__address = (self.__host, self.__port)
        self.__sock = self.__create_socket()

    def __create_socket(self):
        sock = socket()
        sock.bind(self.__address)
        return sock

    def connect(self):
        self.__sock.listen(5)
        while True:
            try:
                connfd,addr = self.__sock.accept()
                print('Connect from:',addr)
            except KeyboardInterrupt:
                self.__sock.close()
                db.close()
                break
            swp = SearchWordProcess(connfd)
            swp.start()

class SearchWordHandle:
    def __init__(self,connfd):
        self.__connfd = connfd # type:socket
        self.__name = ''

    def handle(self):
        pass

    def register(self,mesg):
        name = mesg.split(' ')[0]
        passwd = mesg.split(' ')[1]
        if db.register(name,passwd):
            self.__connfd.send(b'OK')
        else:
            self.__connfd.send(b'FAIL')

    def login(self, mesg):
        name = mesg.split(' ')[0]
        passwd = mesg.split(' ')[1]
        if db.login(name,passwd):
            self.__connfd.send(b'OK')
            self.__name = name
        else:
            self.__connfd.send(b'FAIL')

    def search_word(self, word):
        mean = db.search_word(word,self.__name)
        self.__connfd.send(mean.encode())

    def check_history(self):
        history_tuple = db.check_history(self.__name)
        if not history_tuple:
            self.__connfd.send('没有历史记录！！！\n'.encode())
            sleep(0.1)
            self.__connfd.send(b'##')
            return
        for item in history_tuple:
            time_str = item[2].strftime("%Y-%m-%d %H:%M:%S")
            history_str = item[0]+'   '+item[1]+'\t'+time_str
            self.__connfd.send((history_str+'\n').encode())
        sleep(0.1)
        self.__connfd.send(b'##')


class SearchWordProcess(Process):
    def __init__(self,connfd):
        super().__init__()
        self.__connfd = connfd # type:socket
        self.__handle = SearchWordHandle(self.__connfd)

    def recv(self):
        while True:
            mesg = self.__connfd.recv(1024).decode().split(' ',1)
            if mesg[0] == 'R':
                self.__handle.register(mesg[1])
            elif mesg[0] == 'L':
                self.__handle.login(mesg[1])
            elif mesg[0] == 'Q':
                self.__handle.search_word(mesg[1])
            elif mesg[0] == 'H':
                self.__handle.check_history()
            elif mesg[0] == 'E' or not mesg :
                print('客户端退出！！！')
                break

    def send(self):
        pass

    def run(self) -> None:
        db.cursor()
        self.recv()
        db.cur.close()
        self.__connfd.close()

if __name__ == '__main__':
    db = SearchWordSQL() # 将数据库对象设置为全局变量,而游标在每一个子进程中创建
    tcp = SearchWordTCP()
    tcp.connect()