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
        while True:
            option = input('请输入选项：')
            if option == '1':
                if self.__controller.login():
                    self.__menu2()
            elif option == '2':
                self.register()
            elif option == '3':
                exit()


    def __select_menu_2(self):
        self.__menu2()

    def register(self):
        if self.__controller.register() == 2:
            print('注册成功！！！')
            consequence = input('请问是否登陆(y/n):')
            if consequence == 'y':
                self.__select_menu_2()
            else:
                return
        elif self.__controller.register() == 1:
            print('用户名和密码不能有空格！！！')
            return
        else:
            print('用户名已存在,注册失败！！！')

    def main(self):
        while True:
            self.__menu1()
            self.__select_menu()



class SearchWordController:
    def __init__(self):
        self.__sock = SearchWordTCP().connect_server()

    def login(self) -> bool:
        pass

    def register(self) -> int:
        user_name = input('请输入用户名:')
        user_passwd = input('请输入密码:')
        if ' ' in user_passwd or ' ' in user_name:
            return 1
        self.__sock.send(('R %s %s'%(user_name,user_passwd)).encode())
        mesg = self.__sock.recv(1024)
        if mesg == b'OK':
            return 2
        else:
            return 3


class SearchWordTCP:
    def __init__(self):
        self.__host = '127.0.0.1'
        self.__port = 8888
        self.__address = (self.__host, self.__port)
        self.__sock = socket()

    def connect_server(self):
        self.__sock.connect(self.__address)
        return self.__sock

if __name__ == '__main__':
    view = SearchWordView()
    view.main()