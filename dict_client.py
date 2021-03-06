"""
在线字典 客户端
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

    def __select_menu_1(self):
        while True:
            self.__menu1()
            option = input('请输入选项：')
            if option == '1':
                self.__login()
            elif option == '2':
                self.__register()
            elif option == '3':
                self.__controller.exit()
                print('谢谢使用！！！')
                break
            else:
                print('输入有误！！！')

    def __select_menu_2(self):
        while True:
            self.__menu2()
            option = input('请输入选项：')
            if option == '1':
                self.__search_word()
            elif option == '2':
                self.__controller.check_history()
            elif option == '3':
                break
            else:
                print('输入有误！！！')

    def __register(self):
        user_name = input('请输入用户名:')
        user_passwd = input('请输入密码:')
        result = self.__controller.register(user_name,user_passwd)
        if result == 2:
            print('注册成功！！！')
            consequence = input('请问是否登陆(y/n):')
            if consequence == 'y':
                if self.__controller.login(user_name,user_passwd):
                    print('登录成功！！！')
                self.__select_menu_2()
            else:
                return
        elif result == 1:
            print('用户名和密码不能有空格！！！')
            return
        else:
            print('用户名已存在,注册失败！！！')

    def __login(self):
        user_name = input('请输入用户名:')
        user_passwd = input('请输入密码:')
        if self.__controller.login(user_name,user_passwd):
            print('登录成功！！！')
            self.__select_menu_2()
        else:
            print('用户名或密码错误,登录失败！！！')

    def main(self):
        self.__select_menu_1()

    def __search_word(self):
        while True:
            word = input('请输入单词(输入 ## 退出)：')
            if word == '##':
                return
            print("%s: %s"%(word,self.__controller.search_word(word)))


class SearchWordController:
    def __init__(self):
        self.__sock = SearchWordTCP().connect_server()

    def login(self,user_name, user_passwd) -> bool:
        self.__sock.send(('L %s %s' % (user_name, user_passwd)).encode())
        mesg = self.__sock.recv(1024)
        if mesg == b'OK':
            return True
        else:
            return False

    def register(self,user_name,user_passwd) -> int:
        if ' ' in user_passwd or ' ' in user_name:
            return 1
        self.__sock.send(('R %s %s'%(user_name,user_passwd)).encode())
        mesg = self.__sock.recv(1024)
        if mesg == b'OK':
            return 2
        else:
            return 3

    def exit(self):
        self.__sock.send(b'E')

    def search_word(self,word):
        self.__sock.send(('Q %s'%word).encode())
        mesg = self.__sock.recv(1024)
        return mesg.decode()

    def check_history(self):
        self.__sock.send(b'H')
        while True:
            mesg = self.__sock.recv(1024).decode()
            if mesg == '##':
                break
            print(mesg, end='') # end = ''会导致无法打印


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