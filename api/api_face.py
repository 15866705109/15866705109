'''
封装所有接口请求
'''
from face_api_test.api import path_setting
from face_api_test.api.base_api import BaseApi
import jmespath

class Testapi(BaseApi):


    def __init__(self):
        self.data = self.api_load(path_setting.APYAML_CONFIG)


    '''
        订单流水接口
    '''
    #todo:用装饰器解决参数替换
    def consultation_orders(self, year, month, page):
        self.params["year"] = year
        self.params["month"] = month
        self.params["page"] = page
        return self.api_send(self.data["test_consultation_orders"])
    '''
    通过此接口获取登录用户的counselor_id
    '''
    def personal_center(self):
        r = self.api_send(self.data["personal_center"])
        url = r["data"]["icon"]["data"][0]["url"]
        counseller_id = url.split("=")[-1]
        return counseller_id



    def login(self):
        r = self.get_cookie(self.data["login"])
        with open(path_setting.GET_COOKIE, 'w+') as f:
            f.write(str(r))

    def get_user_id(self):
        r = self.api_send(self.data["login"])
        user_id = r["data"]["user_id"]
        return user_id

    '''
    视频面诊1V1发起接口
    '''
    def prepare_one2one(self, user_gender, user_age, counsellor_id, referer, user_has_aesthetic_medicine, user_target_project):
        self.params["user_gender"] = user_gender
        self.params["user_age"] = user_age
        self.params["counsellor_id"] = counsellor_id
        self.params["referer"] = referer
        self.params["user_has_aesthetic_medicine"] = user_has_aesthetic_medicine
        self.params["user_target_project"] = user_target_project
        return self.api_send(self.data["prepare_one2one"])

    '''
    视频面诊订单列表接口
    '''
    def consultation_order_list(self, page):
        self.params["page"] = page
        return self.api_send(self.data["consultation_order_list"])


    '''
    视频面诊订单详情请求封装
    '''

    def consultation_order_detail(self):
        return self.api_send(self.data["consultation_order_detail"])


    '''
    获取订单支付参数
    '''

    def order_payment(self):
       return self.api_send(self.data["order_payment"])

    '''
    正式发起1V1视频面诊
    '''

    def launch_one2one(self, trace_id, order_no):
        self.params["trace_id"] = trace_id
        self.params["order_no"] = order_no
        return self.api_send(self.data["launch_one2one"])

    def get_consultation_record(self, cookie, consultation_record_id):
        self.params["Cookie"] = cookie
        self.params["consultation_record_id"] = consultation_record_id
        return self.api_send(self.data["get_consultation_record"])
    '''
    取消订单接口
    '''
    def order_cancel(self):
        return  self.api_send(self.data["order_cancel"])

    '''
    正式发起派单请求
    '''
    def launch_dispatch(self, order_no, traceId):
        self.params["order_no"] = order_no
        self.params["traceId"] = traceId
        return self.api_send(self.data["launch_dispatch"])

    '''
    尝试发起派单请求
    '''
    def prepare_dispatch(self, user_gender, user_age, referer, user_has_aesthetic_medicine, user_target_project, counsellor_id, counsellor_type):
        self.params["user_gender"] = user_gender
        self.params["user_age"] = user_age
        self.params["counsellor_id"] = counsellor_id
        self.params["referer"] = referer
        self.params["user_has_aesthetic_medicine"] = user_has_aesthetic_medicine
        self.params["user_target_project"] = user_target_project
        self.params["counsellor_type"] = counsellor_type
        return self.api_send(self.data["prepare_dispatch"])


    '''
    支付流程中查询订单状态
    '''
    def order_payment_status(self):
        return self.api_send(self.data["order_payment_status"])

    '''
    订单确认页信息
    '''
    def order_info(self, order_no):
        self.params["order_no"] = order_no
        return self.api_send(self.data["order_info"])

    def order_check(self, order_no):
        self.params["order_no"] = order_no
        return self.api_send(self.data["order_check"])

    '''
    订单挂断时接口
    '''
    def report_event(self, user_agent, cookie, event_type, consultation_record_id, device_id="65D3E5E7-DB71-43F3-910D-B0345C752419"):
        self.params["User-Agent"] = user_agent
        self.params["Cookie"] = cookie
        self.params["device_id"] = device_id
        self.params["event_type"] = event_type
        self.params["consultation_record_id"] = consultation_record_id
        return self.api_send(self.data["report_event"])

    def current_dispatch_ping(self):
        return self.api_send(self.data["current_dispatch_ping"])

    '''
    派单匹配成功接口，用户获取当前面诊派单接口
    '''
    def get_current_dispatch_info(self):

       return self.api_send(self.data["get_current_dispatch_info"])

    '''
    用户创建面诊派单接口
    '''
    def start_dispatch(self):
        pass
    '''
    用户取消面诊派单接口
    '''
    def cancel_dispatch(self, trigger_source):
        self.params["trigger_source"] = trigger_source
        return self.api_send(self.data["cancel_dispatch"])

    '''
    面诊师弹出卡片信息接口,去掉面诊时长/面诊人数/粉丝数 展示 显示 好评率/接通率 or 好评率/有效面诊
    '''
    def consultant(self):
        pass
    '''
    视频面诊工作台-首页
    '''
    def home(self, doctor_id):
        self.params["doctor_id"] = doctor_id
        return self.api_send(self.data["home"])
    '''
    视频面诊工作台 - 待抢面诊派单 
    '''
    def current_dispatch_task_list(self, device_id,cookie):
        self.params['Cookie'] = cookie
        self.params["device_id"] = device_id
        return self.api_send(self.data["current_dispatch_task_list"])

    '''
    视频面诊工作台 - 待抢面诊派单数量
    '''
    def current_dispatch_task_count(self):
        return self.api_send(self.data["current_dispatch_task_count"])
    '''
    面诊报告列表
    '''
    def reports(self, page_num, page_size, report_status_type, report_time_type, counsellor_id, record_type):
        self.params["page_num"]=page_num
        self.params["page_size"] = page_size
        self.params["report_status_type"] = report_status_type
        self.params["report_time_type"] = report_time_type
        self.params["counsellor_id"] = counsellor_id
        self.params["record_type"] = record_type
        return self.api_send(self.data["reports"])


    def consultant(self):
        pass



    '''
    推荐位视频面诊频道推荐面诊顾问
    '''
    def recommend_counsellors(self,version):
        self.params['version']= version
        #print(self.api_send(self.data['recommend_counsellors']))
        return self.api_send(self.data['recommend_counsellors'])


    '''
    feed流视频面诊频道tab 面诊顾问列表
    '''

    # todo:用装饰器解决参数替换
    def counsellors(self,tab_id,page,version):
        self.params["tab_id"] = tab_id
        self.params["page"] = page
        self.params["version"] = version
        #print(self.api_send(self.data['counsellors']))
        return self.api_send(
            self.data['counsellors'])
    '''
    请求卡片：查看封禁信息
    '''
    def block_info(self):
        return self.api_send(self.data['block_info'])


    '''
    请求卡片：判断是否新用户，获取消费者信息
    '''
    def customer(self,counsellor_id,doctor_id):
        self.params['counsellor_id'] = counsellor_id
        self.params['doctor_id'] = doctor_id
        return self.api_send(self.data['customer'])




    '''
    请求卡片：面诊师表单获取上一次信息接口
    '''

    def consultation_apply_form_info(self,doctor_id,counsellor_id,record_type):
        self.params['doctor_id'] = doctor_id
        self.params['counsellor_id'] = counsellor_id
        self.params['record_type'] = record_type
        return self.api_send(self.data["consultation_apply_form_info"])

    '''
    视频面诊工作台-开启面诊操作 
    '''
    def start_consultation(self):
        return self.api_send(self.data['start_consultation'])

    '''
    视频面诊工作台-停止面诊操作 
    '''
    def stop_consultation(self):
        return self.api_send(self.data['stop_consultation'])

    '''
    视频面诊工作台-已抢面诊派单列表
    '''
    def finished_dispatch_task_list(self):
        return self.api_send(self.data['finished_dispatch_task_list'])

    '''
    视频面诊工作台-面诊师抢派单
    '''
    def join_dispatch(self, cookie, dispatch_task_id):
        self.params["cookie"] = cookie
        self.params["dispatch_task_id"] = dispatch_task_id
        return self.api_send(self.data['join_dispatch'])

    '''
        打星评价获取
    '''
    def evaluate_items(self):
        return self.api_send(self.data['evaluate_items'])

    '''
      投诉意见
    '''
    def complaint(self):
        print(self.api_send(self.data['complaint']))
        return self.api_send(self.data['complaint'])

    '''
    推荐袋数据获取
    '''
    def get_recommended_bag(self):
        return self.api_send(self.data['get_recommended_bag'])

    '''
    添加推荐袋
    '''
    def add_recommended_bag(self):
        return self.api_send(self.data['add_recommended_bag'])

    '''
    推荐袋搜索
    '''
    def search_service(self):
        return self.api_send(self.data['search_service'])

    '''
    删除推荐袋
    '''
    def delete_recommended_bag(self):
        return self.api_send(self.data['delete_recommended_bag'])







if __name__ == '__main__':
     #Testapi().finished_dispatch_task_list()
    # Testapi().consultation_orders("")
    #Testapi().consultation_orders("2020", "04", "1")
    # Testapi().consultation_order_list()
    # Testapi().consultation_order_detail()
    # Testapi().order_payment()
    # Testapi().order_cancel()
    # Testapi().launch_dispatch()
    # Testapi().order_payment_status()
    # Testapi().order_info()
    # Testapi().order_check()
    # Testapi().prepare_one2one()

    #Testapi().get_user_id()
    #Testapi().consultation_apply_form_info(1,1,1)
    Testapi().complaint()





