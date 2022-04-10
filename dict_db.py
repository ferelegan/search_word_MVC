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