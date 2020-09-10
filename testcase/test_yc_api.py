import pytest
import json
import jsonpath
import jmespath
from face_api_test.api import path_setting
from face_api_test.api.api_face import Testapi
from face_api_test.api.base_api import BaseApi
from face_api_test.database.db_manage import DB
from face_api_test.testcase.ids_list import get_ids
from face_api_test.testcase.process import Process



class Test_api:
    # 拿到ias里的返回值
    yc_data= BaseApi().api_load(path_setting.YUCHAO_TEST_DATA)
    yc_data1 = BaseApi().api_load(path_setting.YUCHAO_TEST_DATA)
    # 拿到path_setting文件里的传参
    orders_counsellors_case, orders_counsellors_data = get_ids(yc_data, 'recommend_counsellors')
    orders_param_case, orders_param_data = get_ids(yc_data, 'consultation_param')
    orders_customer_case,orders_customer_data = get_ids(yc_data,'customer')
    orders_consultation_apply_form_info_case , orders_consultation_apply_form_info_data = get_ids(yc_data,'consultation_apply_form_info')

    #
    orders_join_dispatch_case,orders_join_dispatch_data = get_ids(yc_data,'join_dispatch')




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
        print('测试传参',a)
        #assistant = jmespath.seiinarch("counsellors[*].{Name:name,assistant:is_assistant}",a) #拿到接口里医生对应的good_at
        connect_rate = (jmespath.search("counsellors[*].{Name:name,connect_rate:connect_rate}",a))
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
        # 是否在线
        status = (jmespath.search("counsellors[*].{Name:name,status:status}",a))
        print(status)
        Statuslist = []
        for i in status:
            user1 = i['Name']
            status1 = i['status']
            if status1 == 2:
                Statuslist.append({user1:status1})
        print('在线的面诊时是',Statuslist)

        userid = jsonpath.jsonpath(r,"$..user_id.") #拿到接口里所有的userid
        sql = "SELECT good_at FROM consultation_counsellor WHERE user_id IN {}".format(tuple(userid))
        a = DB().query_db(sql)
        print("999999",a[0]["good_at"])


    def test_block_info(self):  #查看封禁信息
        a = Testapi().block_info()['data']['block_info']
        print(a)
        assert a['status'] == 0

    @pytest.mark.parametrize("param", orders_customer_data, ids=orders_customer_case)  # 接收参数
    def test_customer(self,param):
        a = Testapi().customer(param['counsellor_id'],param['doctor_id'])['data']
        print(a)
        assert a['has_record'] == True
        if a['has_record'] == True and a['counsellor_type'] == 1:
            print('新用户')
        elif a['has_record'] == False and a['counsellor_type'] == -1:
            print('老用户')
        elif a['counsellor_type'] == None:
            print('传参错误')


    #面诊师表单获取上一次信息接口
    @pytest.mark.parametrize('param',orders_consultation_apply_form_info_data, ids=orders_consultation_apply_form_info_case)
    def test_consultation_apply_form_info(self,param):
        a = Testapi().consultation_apply_form_info(param['doctor_id'],param['counsellor_id'],param['record_type'])
        assert a['error'] == 0
        print(a)


    #开启面诊
    def test_start_consultation(self):
        a = Testapi().start_consultation()
        if a['error_code'] == -1:
            print('当前医生已下线，无法使用视频面诊')

    #关闭面诊
    def test_stop_consultation(self):
        a = Testapi().stop_consultation()
        if a['error_code'] == -1:
            print('当前医生已下线，无法使用视频面诊')


    #已抢面诊派单列表
    def test_finished_dispatch_task_list(self):
        a = Testapi().finished_dispatch_task_list()
        print(a)
        assert a['error_extra'] == None


    #轮询抢单列表
    @pytest.mark.parametrize("param", orders_join_dispatch_data, ids = orders_join_dispatch_case)
    def test_join_dispatch(self, param):
        consultation_record_id, order_no, dispatch_task_id = Process().dispatch_op(param)
        print('111111111', dispatch_task_id)
        Testapi().report_event(param["user_agent"], param["cookie"], 8,
                               consultation_record_id, param["device_id_lanch"])
        # 用户加入
        Testapi().report_event("", "", 2, consultation_record_id, param["device_id_recive"])
        Process().event_order_check(consultation_record_id, param, 7, order_no)
        # a = Tgestapi.join_dispatch(param['cookie'],dispatch_task_id)
        # print(a,00000)



    # 打星评价
    def test_evaluate_items(self):
        a = Testapi().evaluate_items()
        print(a)

    #投诉意见
    def complaint(self):   #
        a = Testapi.complaint()
        print(a)


    #推荐袋数据获取
    def get_recommended_bag(self):
        a =  Testapi.get_recommended_bag()

    #添加推荐袋

    def add_recommended_bag(self):
        a = Testapi.add_recommended_bag()

    #推荐袋搜索

    def search_service(self):
        a = Testapi.search_service()

    #删除推荐袋

    def delete_recommended_bag(self):
        a = Testapi.delete_recommended_bag()
