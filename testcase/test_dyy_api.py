import pytest
import self as self

from face_api_test.api import path_setting
from face_api_test.api.api_face import Testapi
from face_api_test.api.base_api import BaseApi
from face_api_test.database.db_manage import DB
from face_api_test.testcase.ids_list import get_ids


class Test_api:
    orders_param_case, orders_param_data = get_ids('consultation_orders_param')
    orders_count_case, orders_count_data = get_ids("consultation_orders_count")
    orders_commission_case, orders_commission_data = get_ids("consultation_orders_commission")

    @classmethod
    def setup_class(cls):
        cls.login = Testapi().login()



    # 测试传参有效性
    @pytest.mark.parametrize("param", orders_param_data, ids=orders_param_case)
    def test_consultation_orders_param(self, param):
        r = Testapi().consultation_orders(param["year"], param["month"], param["page"])
        print(r)
        assert r["error"] == param["asser"]
        if r["data"]["total_income"] == 0:
            assert r["data"]["total_income"] == 0
        if r["data"]["total_income"] == None:
            assert r["data"]["total_income"] == None

    # 测试订单总数与对应月份是否一致
    @pytest.mark.parametrize("param", orders_count_data, ids=orders_count_case)
    def test_consultation_orders_count(self, param):
        counseller_id = Testapi().personal_center()
        r = Testapi().consultation_orders(param["year"], param["month"], param["page"])
        firstDay, lastDay = DB().getFirstAndLastDay(param["year"], param["month"])
        sql = "select count(id) as count from " \
              "`consultation_order` where `counsellor_id`= '{}' " \
              "and status=6 and payment_time >= '{}' " \
              "and payment_time < '{}'".format(counseller_id, firstDay, lastDay)
        DB().get_conn()
        a = DB().query_db(sql)

        assert r["data"]["order_count"] == a[0]["count"]


    # 测试订单的总佣金是否与月份一致
    @pytest.mark.parametrize("param", orders_commission_data, ids=orders_commission_case)
    def test_consultation_orders_commission(self, param):
        counseller_id = Testapi().personal_center()
        r = Testapi().consultation_orders(param["year"], param["month"], param["page"])
        print(r)
        firstDay, lastDay = DB().getFirstAndLastDay(param["year"], param["month"])
        sql = "select sum(commission_amount) as commission from `consultation_order`" \
              " where `counsellor_id`= '{}' and status=6 and " \
              "payment_time >= '{}' and " \
              "payment_time < '{}'".format(counseller_id, firstDay, lastDay)
        DB().get_conn()
        a = DB().query_db(sql)
        print(a)
        print(r["data"]["total_income"])
        # print(a[0]["commission"])
        assert r["data"]["total_income"] == a[0]["commission"]

    # @pytest.mark.me
    def test_prepare_one2one(self):
        r = Testapi().prepare_one2one()
        print(r)

    def test_order_check(self):
        r = Testapi().order_check()
        print(r)

    @pytest.mark.parametrize("trace_id", ["7a70dbb478752337face88f50485f393", ])
    def test_launch_one2one(self, trace_id):
        r = Testapi().launch_one2one(trace_id)
        print(r)

    def test_consultation_order_list(self):
        r = Testapi().consultation_order_list()
        print(r)

    def test_consultation_order_detail(self):
        r = Testapi().consultation_order_detail()
        print(r)

    def test_order_payment(self):
        r = Testapi().order_payment()
        print(r)

    def test_order_cancel(self):
        r = Testapi().order_cancel()
        print(r)

    def test_order_payment_status(self):
        r = Testapi().order_payment_status()
        print(r)

    def test_order_info(self):
        r = Testapi().order_info()
        print(r)

    def test_order_check(self):
        r = Testapi().order_check()
        print(r)

    def test_cancel_dispatch(self):
        r = Testapi().cancel_dispatch()
        print(r)

    # todo:需要确认怎么获取有效抢单
    def test_get_current_dispatch_info(self):
        r = Testapi().get_current_dispatch_info()
        print(r)

    def test_launch_dispatch(self):
        r = Testapi().launch_dispatch()
        print(r)

    # todo；感觉没必要写
    def test_current_dispatch_task_list(self):
        r = Testapi().current_dispatch_task_list()
        print(r)

    def test_current_dispatch_task_count(self):
        r = Testapi().current_dispatch_task_count()
        print(r)

    # todo:需要调用开启和关闭面诊断言信息
    def test_home(self):
        r = Testapi().home()
        print(r)

    def test_reports(self):
        r = Testapi().reports()
        print(r)


if __name__ == '__main__':
    pass
