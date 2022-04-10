"""
在线字典 数据库处理
"""
from pymysql import *


class SearchWordSQL:
    def __init__(self):
        self.__kwargs = {
            "host":'localhost',
            "port":3306,
            "user":'root',
            "password":'123456',
            "database":'dict',
            "charset":'utf8'
        }
        self.db = connect(**self.__kwargs)

    def cursor(self):
        self.cur = self.db.cursor()

    def close(self):
        self.db.close()

    def register(self,name,passwd):
        sql = 'insert into user (name,password) values (%s,%s);'
        try:
            self.cur.execute(sql,[name,passwd])
        except:
            return False
        else:
            self.db.commit()
            print('数据注入成功！！！')
            return True

    def login(self, name, passwd):
        """
        我写的 效率不高有for循环！
        sql = 'select name,password from user;'
        self.cur.execute(sql) # [(name,password),(name,password),...]
        for item in self.cur:
            if name in item[0] and passwd in item[1]:
                return True
        return False
        """
        # 老师的
        sql = 'select name from user where name = %s and password = %s;'
        self.cur.execute(sql,[name,passwd])
        if self.cur.fetchone():
            return True
        else:
            return False


if __name__ == '__main__':
    sql = SearchWordSQL()
    sql.cursor()
    if sql.login('mary','123456'):
        print('登陆成功!!!')