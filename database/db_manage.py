'''
数据库连接，查询操作封装
'''

import pymysql
from pymysql import OperationalError

from gm.api.base_api import BaseApi


class DB:
    def __init__(self):
        self.data = BaseApi().api_load("../api/config.yaml")
        print(self.data)

    # 连接数据库
    def get_conn(self):
        try:
            conn = pymysql.connect(**self.data["ddoctor"])
            return conn
        except OperationalError as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    # 查询数据库
    def query_db(self, sql):
        conn = self.get_conn()
        # 2. 建立游标
        cur = conn.cursor()
        # 3. 执行sql
        cur.execute(sql)
        # 4. 获取数据
        result = cur.fetchall()
        print(result)
        return result

    # 关闭数据库
    def close(self):
        self.conn.close()


if __name__ == '__main__':
    DB().query_db("select * from consultation_counsellor where id ='00005924604511e5a2a200163e004883'")
