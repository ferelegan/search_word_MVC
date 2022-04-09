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
        self.cur = self.db.cursor()

    def test(self):
        sql = 'insert into user (name,password) values (%s,%s);'
        self.cur.execute(sql,["mary","123456"])
        self.db.commit()

    def close(self):
        self.cur.close()
        self.db.close()


if __name__ == '__main__':
    db = SearchWordSQL()
    db.test()