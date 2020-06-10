import pytest
import json
import jsonpath
import jmespath
from face_api_test.api import path_setting
from face_api_test.api.api_face import Testapi
from face_api_test.api.base_api import BaseApi
from face_api_test.database.db_manage import DB
from face_api_test.testcase.ids_list import get_ids


class Test_api:
    yc_data= BaseApi().api_load(path_setting.YUCHAO_TEST_DATA) #拿到ias里的返回值
    orders_counsellors_case, orders_counsellors_data = get_ids(yc_data, 'recommend_counsellors')
    orders_param_case, orders_param_data = get_ids(yc_data, 'consultation_param') #拿到yu_yaml文件里的传参
    orders_customer_case,orders_customer_data = get_ids(yc_data,'customer')

    @classmethod
    def setup_class(cls):
        cls.login = Testapi().login()
    #面诊推荐位
    @pytest.mark.parametrize("param", orders_counsellors_data, ids=orders_counsellors_case)  # 接收参数
    def test_recommend_counsellors(self,param):
        a = Testapi().recommend_counsellors(param['version'])['data']['tabs']  #截取
        name = jsonpath.jsonpath(a,'$..name')
        print(name)
        b = Testapi().recommend_counsellors(param['version'])#截取

        assert b['error_extra'] == None

    #feed流
    @pytest.mark.parametrize("param", orders_param_data, ids=orders_param_case) #接收参数
    def test_counsellors(self,param):
        r = Testapi().counsellors(param["tab_id"], param["page"], param["version"])#接口里的值赋值到r
        a = r['data']
        good = jmespath.search("counsellors[*].{Name:name,Good_at:good_at}",a) #拿到接口里医生对应的good_at
        print(good)
        b = r['data']['counsellors'] #每个tab下所有的值
        print(b)
        for  i in good:       #列表值获取的有点问题， 对比不了，稍后该
            if i not in b:
                print('包含')
            else:
                print('不包含')


        userid = jsonpath.jsonpath(r,"$..user_id.") #拿到接口里所有的userid
        # sql = "SELECT good_at FROM consultation_counsellor WHERE user_id IN {}".format(tuple(userid))
        # a = DB().query_db(sql)
        # print("999999",a[0]["good_at"])



    def test_block_info(self):  #查看封禁信息
        a = Testapi().block_info()['data']['block_info']
        print(a)
        assert a['status'] == 0

    @pytest.mark.parametrize("param", orders_customer_data, ids=orders_customer_case)  # 接收参数
    def test_customer(self,param):  #没找到传参怎么判断新老用户
        a = Testapi().customer(param['counsellor_id'],param['doctor_id'])['data']
        assert a['has_record'] == True
        if a['has_record'] == True:
            print('新用户')
        else:
            print('老用户')

    def test_consultation_apply_form_info(self):
        a = Testapi().consultation_apply_form_info()

        print(a)

    def test_start_consultation(self):
        a = Testapi().start_consultation()
        print(a)

    def test_stop_consultation(self):
        a = Testapi().stop_consultation()
        print(a)

    def test_finished_dispatch_task_list(self):
        a = Testapi().finished_dispatch_task_list()
        print(a)

    def test_join_dispatch(self):
        a = Testapi().join_dispatch()
        assert a['message'] == '没有找到指定的面诊派单任务'
        print(a['message'])

