"""
在线字典 数据库处理
"""
from pymysql import *


class SearchWordSQL:
    def __init__(self):
        self.kwargs = {
            "host":'localhost',
            "port":3306,
            "user":'root',
            "password":'123456',
            "database":'dict',
            "charset":'utf8'
        }
        self.db = connect(**self.kwargs)
        self.cur = self.db.cursor()

    def test(self):
        sql = 'select * from words limit 10;'
        self.cur.execute(sql)
        for item in self.cur:
            print(item)