"""
在线字典 服务端
"""

from multiprocessing import Process
from socket import *
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
            connfd,addr = self.__sock.accept()
            swp = SearchWordProcess(connfd)
            swp.start()

class SearchWordHandle:
    def __init__(self,connfd):
        self.__connfd = connfd # type:socket
        self.__sql = SearchWordSQL()

    def handle(self):
        pass

    def register(self,mesg):
        name = mesg.split(' ')[0]
        passwd = mesg.split(' ')[1]
        sql = 'insert into user (name,password) values (%s,%s);'
        try:
            self.__sql.cur.execute(sql,[name,passwd])
        except:
            self.__connfd.send(b'FAIL')
        else:
            self.__sql.db.commit()
            # print('数据注入成功！！！')
            self.__connfd.send(b'OK')



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
                pass
            elif mesg[0] == 'Q':
                pass
            elif mesg[0] == 'H':
                pass
            elif mesg[0] == 'E':
                pass


    def send(self):
        pass


    def run(self) -> None:
        self.recv()

if __name__ == '__main__':
    tcp = SearchWordTCP()
    tcp.connect()