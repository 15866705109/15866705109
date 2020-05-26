import pytest

from face_api_test.api import path_setting
from face_api_test.api.api_face import Testapi
from face_api_test.api.base_api import BaseApi


class Test_api:

    data = BaseApi().api_load(path_setting.TEST_API_DATA)

    @classmethod
    def setup_class(cls):
        cls.login = Testapi().login()


    @pytest.mark.parametrize("param", data['consultation_orders'])
    def test_consultation_orders(self, param):
        r = Testapi().consultation_orders(param["year"], param["month"], param["page"])
        print(r)
        assert r["error"] == param["asser"]

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