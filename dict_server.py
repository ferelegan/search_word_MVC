"""
在线字典 服务端
"""

from multiprocessing import Process
from socket import *

class SearchWordTCP:
    def __init__(self):
        self.__host = '0.0.0.0'
        self.__port = '8888'
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

class SearchWordHandle:
    def handle(self):
        pass

class SearchWordProcess(Process):
    def __init__(self,connfd):
        super().__init__()
        self.__connfd = connfd

    def recv(self):
        pass

    def send(self):
        pass

    def handle(self):
        handle = SearchWordHandle()
        handle.handle()

    def run(self) -> None:
        pass

