'''
数据库连接，查询操作封装
'''
import calendar
import datetime

import pymysql
from pymysql import OperationalError

from face_api_test.api import path_setting
from face_api_test.api.base_api import BaseApi


class DB:
    def __init__(self):
        self.host = BaseApi().api_load(path_setting.HOSTYAML_CONFIG)
        self.data = BaseApi().api_load(path_setting.CONFIGYAML_CONFIG)
        print("000000000",self.host)

    # 连接数据库
    def get_conn(self):
        try:
            if self.host["merchant_host"]["url"] == "http://backend.paas-consult.env":
                conn = pymysql.connect(**self.data["consult"])
            else:
                conn = pymysql.connect(**self.data["merchant"])
            return conn
        except OperationalError as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    # 查询数据库
    def query_db(self, sql):
        conn = self.get_conn()
        # 2. 建立游标
        cur = conn.cursor(pymysql.cursors.DictCursor)
        # 3. 执行sql
        cur.execute(sql)
        # 4. 获取数据
        result = cur.fetchall()
        print(result)
        return result

    # 关闭数据库
    def close(self):
        conn = self.get_conn()
        conn.close()

    def getFirstAndLastDay(self, year, month):
        # 获取当前月的第一天的星期和当月总天数
        weekDay, monthCountDay = calendar.monthrange(year, month)
        # 获取当前月份第一天
        firstDay = datetime.date(year, month, day=1)
        # 获取当前月份最后一天
        # lastDay = datetime.date(year, month, day=monthCountDay)
        # 返回第一天和最后一天
        lastDay = datetime.date(year, month, day=monthCountDay) + datetime.timedelta(days=1)
        return firstDay, lastDay


if __name__ == '__main__':
   # a,b=DB().getFirstAndLastDay(2020,4)
   # print(a,b)
   #  DB().get_conn()
    DB().query_db("select * from consultation_counsellor where id ='00005924604511e5a2a200163e004883'")
