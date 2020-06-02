import pytest
import jmespath

from face_api_test.api import path_setting
from face_api_test.api.api_face import Testapi
from face_api_test.api.base_api import BaseApi
from face_api_test.database.db_manage import DB
from face_api_test.testcase.ids_list import get_ids


class Test_api:
    data = BaseApi().api_load(path_setting.TEST_API_DATA)
    orders_param_case, orders_param_data = get_ids(data, 'consultation_orders_param')
    orders_count_case, orders_count_data = get_ids(data, "consultation_orders_count")
    orders_commission_case, orders_commission_data = get_ids(data, "consultation_orders_commission")
    prepare_one2one_case, prepare_one2one_data = get_ids(data, "prepare_one2one_param")
    launch_one2one_case, launch_one2one_data = get_ids(data, "launch_one2one")
    lanunch_one2one_ecp_case, lanunch_one2one_ecp_data = get_ids(data, "lanunch_one2one_ecp")
    reports_case, reports_data = get_ids(data, "reports")
    consultation_order_list_case, consultation_order_list_data = get_ids(data, "consultation_order_list")
    cancel_dispatch_case, cancel_dispatch_data = get_ids(data, "cancel_dispatch")
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
        count = DB().query_db(sql)
        print(count)
        print(r["data"]["total_income"])
        assert r["data"]["total_income"] == count[0]["commission"]

    @pytest.mark.parametrize("param", prepare_one2one_data, ids=prepare_one2one_case)
    def test_prepare_one2one_param(self, param):
        if param["counsellor_id"] == "":
            counseller_id = Testapi().personal_center()
            r = Testapi().prepare_one2one(param["user_gender"], param["user_age"], counseller_id,
                                          param["referer"],
                                          param["user_has_aesthetic_medicine"], param["user_target_project"])
        else:
            r = Testapi().prepare_one2one(param["user_gender"], param["user_age"], param["counsellor_id"], param["referer"],
                                      param["user_has_aesthetic_medicine"], param["user_target_project"])

        if r["error"] == 0:
            print(r["data"]["order_status"], param["assert"])
            assert r["data"]["order_status"] == param["assert"]
        if r["error"] == 1 and r["error_code"] == 96003:
            print(r["message"], param["assert"])
            assert r["message"] == param["assert"]
        if r["error"] == 1 and r["error_code"] == 96006:
            print(r["message"])
            assert r["message"] == param["assert"]
        if r["error"] == 1 and r["error_code"] == -1:
            print(r["message"])
            assert r["message"] == param["assert"]
        if r["error"] == 1 and r["error_code"] == 96005:
            print(r["message"])
            assert r["message"] == param["assert"]

    @pytest.mark.parametrize("param", launch_one2one_data, ids=launch_one2one_case)
    def test_launch_one2one(self, param):
        # trace_id = BaseApi().trace_id()
        # print("=====", trace_id)
        r = Testapi().prepare_one2one(param["user_gender"], param["user_age"], param["counsellor_id"],
                                      param["referer"],
                                      param["user_has_aesthetic_medicine"], param["user_target_project"])

        if r["error"] == 0:
            order_no = r["data"]["order_no"]
            result = Testapi().launch_one2one(BaseApi().trace_id(), order_no)
            if result["error"] == 0:
                print("000000000", result["error"])
                assert result["error"] == param["assert"]
        if r["error"] == 1 and r["error_code"] == 96004:
            print("-------", r["message"])
            assert r["message"] == param["assert"]
        if r["error"] == 1 and r["error_code"] == 96008:
            print("**********", param["trace_id"])
            result = Testapi().launch_one2one(order_no, param["trace_id"])
            print("------",result["message"])
            assert result["message"] == param["assert"]


    @pytest.mark.parametrize("param", lanunch_one2one_ecp_data, ids=lanunch_one2one_ecp_case)
    def test_lanunch_one2one_ecp(self, param):
        r =  Testapi().launch_one2one(param["trace_id"], param["order_no"])
        if r["error_code"] == 96041:
            assert r["message"] == param["assert"]
            print(r["message"])
        if r["error_code"] == 96040:
            print(r["message"])
            assert r["message"] == param["assert"]


    @pytest.mark.parametrize("param", consultation_order_list_data, ids=consultation_order_list_case)
    def test_consultation_order_list(self, param):
        r = Testapi().consultation_order_list(param["page"])
        # # user_id = Testapi().get_user_id()
        # sql = "select count(id) as num from `consultation_order` " \
        #       "where user_id={} and status !=0 and status !=1".format(user_id)
        #
        # total = DB().query_db(sql)
        if len(r["data"]["orders"]) > 0:
            print("1")
            assert len(r["data"]["orders"]) > 0
        if r["error"] == 0 and len(r["data"]["orders"]) == 0:
            # assert r["error"] == 0
            print("%%%%%%",len(r["data"]["orders"]))
            assert len(r["data"]["orders"]) == param["assert"]
        if r["error"] == 1:
            print("&&&&&&",r["message"])
            assert r["message"] == param["assert"]



    #TODO 走流程时解决
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
    #todo:需要模拟流程
    def test_order_info(self):
        r = Testapi().order_info()
        print(r)

    def test_order_check(self):
        r = Testapi().order_check()
        print(r)


    @pytest.mark.parametrize("param", cancel_dispatch_data, ids=cancel_dispatch_case)
    def test_cancel_dispatch(self, param):
        r = Testapi().cancel_dispatch(param["trigger_source"])
        assert r["message"] == param["assert"]

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
        assert r["error"] == 0

    def test_current_dispatch_task_count(self):
        r = Testapi().current_dispatch_task_count()
        assert r["error"] == 0


    def test_home(self):
        r = Testapi().home()
        assert r["error"] == 0


    @pytest.mark.parametrize("param", reports_data, ids=reports_case)
    def test_reports(self, param):
        counsellor_id = Testapi().personal_center()
        r = Testapi().reports(param["page_num"], param["page_size"], param["report_status_type"],
                              param["report_time_type"], counsellor_id, param["record_type"])



if __name__ == '__main__':
    pass
