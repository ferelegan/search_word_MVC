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

    def search_word(self,word,name):
        sql = 'select mean,id from words where word = %s;'
        self.cur.execute(sql,word)
        mean = self.cur.fetchone()
        if not mean:
            return '没有找到单词释义！！！'
        else:
            self.__insert_history(name,mean[1])
            return mean[0]

    def __insert_history(self,name,words_id):
        sql = 'select id from user where name = %s;'
        self.cur.execute(sql, name)
        user_id = self.cur.fetchone()[0]
        sql = 'insert into history (words_id,user_id) values (%s,%s);'
        self.cur.execute(sql, [words_id, user_id])
        self.db.commit()

    def check_history(self,name):
        sql = 'select user.name,words.word,h.time from words right join history as h \
              on h.words_id = words.id left join user on h.user_id = user.id ' \
              'where user.name = "%s"' \
              'order by time desc limit 10;'%(name)
        self.cur.execute(sql)
        return self.cur.fetchall()

# insert into history (words_id,user_id) values ('1','1');

# select user.name,words.word,h.time from words right join history as h
# on h.words_id = words.id left join user on h.user_id = user.id limit 10;

if __name__ == '__main__':
    sql = SearchWordSQL()
    sql.cursor()
    # if sql.login('mary','123456'):
    #     print('登陆成功!!!')

    # print(sql.search_word('word','mary'))

    print(sql.check_history('mary'))