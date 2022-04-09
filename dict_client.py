"""
在线字典 客户端
"""

"""
在线查单词客户端
"""
from socket import *


class SearchWordView:
    def __init__(self):
        self.__controller = SearchWordController()

    def __menu1(self):
        print("""
        ╔===============在线字典=================╗
        |                                        |
        |   --------------首页------------       |
        |   1. 登陆                              |
        |   2. 注册                              |
        |   3. 退出                              |
        |   ------------------------------       |
        |   说明：通过数字键选择菜单             |
        ╚========================================╝
        """)

    def __menu2(self):
        print("""
        ╔===============在线字典=================╗
        |                                        |
        |   -------------查单词------------      |
        |   1. 查单词                            |
        |   2. 历史记录                          |
        |   3. 注销                              |
        |   ------------------------------       |
        |   说明：通过数字键选择菜单             |
        ╚========================================╝
        """)

    def __select_menu(self):
        self.__menu1()
        option = input('请输入选项：')
        if option == '1':
            if self.__controller.login():
                self.__menu2()
        elif option == '2':
            if self.__controller.register():
                consequence = input('请问是否登陆(y/n):')
                if consequence == 'y':
                    self.__menu2()
                else:
                    return
            else:
                print('注册失败！！！')
        elif option == '3':
            exit()


class SearchWordController:
    def __init__(self):
        self.__sock = SearchWordTCP().connect_server()

    def login(self) -> bool:
        pass

    def register(self) -> bool:
        user_name = input('请输入用户名:')
        self.__sock.send(('R %s'%user_name).encode())
        mesg = self.__sock.recv(1024)
        if mesg == b'OK':
            user_passwd = input('请输入密码:')
            return True
        else:
            return False




class SearchWordTCP:
    def __init__(self):
        self.__host = '127.0.0.1'
        self.__port = '8888'
        self.__address = (self.__host, self.__port)
        self.__sock = socket()

    def connect_server(self):
        self.__sock.connect(self.__address)
        return self.__sock
