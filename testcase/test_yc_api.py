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
    # 拿到ias里的返回值
    yc_data= BaseApi().api_load(path_setting.YUCHAO_TEST_DATA)
    yc_data1 = BaseApi().api_load(path_setting.YUCHAO_TEST_DATA)
    # 拿到path_setting文件里的传参
    orders_counsellors_case, orders_counsellors_data = get_ids(yc_data, 'recommend_counsellors')
    orders_param_case, orders_param_data = get_ids(yc_data, 'consultation_param')
    orders_customer_case,orders_customer_data = get_ids(yc_data,'customer')
    orders_consultation_apply_form_info_case , orders_counsellors_data = get_ids(yc_data,'consultation_apply_form_info')




    @classmethod
    def setup_class(cls):
        cls.login = Testapi().login()
    #面诊推荐位
    @pytest.mark.parametrize("param", orders_counsellors_data, ids=orders_counsellors_case)  # 接收参数
    def test_recommend_counsellors(self,param):

        #a = Testapi().recommend_counsellors(param['version'])['data']['tabs']  #截取
        a = Testapi().recommend_counsellors(param['version'])['data']['recommends_counsellors']#截取
        print(a)
        list = []  #接通率大于10
        for i in a:
            user = i['name']
            rew = i['connect_rate']
            if rew >= '10' and rew !='':
                list.append({user: rew})
        print(list)



    #feed流
    @pytest.mark.parametrize("param", orders_param_data, ids=orders_param_case) #接收参数
    def test_counsellors(self,param):
        r = Testapi().counsellors(param["tab_id"], param["page"], param["version"])#接口里的值赋值到r
        a = r['data']
        #print(a)
        #assistant = jmespath.seiinarch("counsellors[*].{Name:name,assistant:is_assistant}",a) #拿到接口里医生对应的good_at
        connect_rate = (jmespath.search("counsellors[*].{Name:name,connect_rate:connect_rate}",a))
        #print(connect_rate)
        counsellorslist = []  #判断接通率
        for i in connect_rate:
            uesr = i['Name']
            rew = i['connect_rate']
            if rew > '50' and rew != '' :
                counsellorslist.append({uesr: rew})
        print('接通率大于50的医生是:',counsellorslist)
        like_rate = (jmespath.search("counsellors[*].{Name:name,like_rate:like_rate}",a)) #拿到接口里的好评率
        #print(like_rate)
        like_rate1 = []   #判断好评率
        for i in like_rate:
            user1 = i['Name']
            rew1 = i['like_rate']
            if rew1 > '50':
                like_rate1.append({user1:rew1})
        print('好评率大于50的医生是:',like_rate1)

        status = (jmespath.search("counsellors[*].{Name:name,Status:status}",a))
        print(status)


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


    #面诊师表单获取上一次信息接口
    @pytest.mark.parametrize('param',orders_counsellors_data, ids=orders_consultation_apply_form_info_case)
    def test_consultation_apply_form_info(self,param):
        a = Testapi().consultation_apply_form_info(param['doctor_id'],param['counsellor_id'],param['record_type'])
        print(a)
    #开启面诊
    def test_start_consultation(self):
        a = Testapi().start_consultation()
        print(a)
    #关闭面诊vi
    def test_stop_consultation(self):
        a = Testapi().stop_consultation()
        print(a)
    #已抢面诊派单列表
    def test_finished_dispatch_task_list(self):
        a = Testapi().finished_dispatch_task_list()
        print(a)
        assert a['error_extra'] == None


    #轮询抢单列表
    def test_join_dispatch(self):
        a = Testapi().join_dispatch()
        assert a['message'] == '没有找到指定的面诊派单任务'
        print(a['message'])


    def test_evaluate_items(self):
        a = Testapi().evaluate_items()
        print(a)

    def complaint(self):
        a = Testapi.complaint()
        print(a)
