'''
封装所有接口请求
'''
from face_api_test.api import path_setting
from face_api_test.api.base_api import BaseApi


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
    视频面诊1V1发起接口
    '''

    def login(self):
        r = self.get_cookie(self.data["login"])
        with open(path_setting.GET_COOKIE, 'w+') as f:
            f.write(str(r))

        # cookies = c.cookies()
        # print(cookies)

    def prepare_one2one(self):
        return self.api_send(self.data["prepare_one2one"])

    '''
    视频面诊订单列表接口
    '''
    def consultation_order_list(self):
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

    def launch_one2one(self, trace_id):
        self.params["trace_id"] = trace_id
        return self.api_send(self.data["launch_one2one"])
    '''
    取消订单接口
    '''
    def order_cancel(self):
        return  self.api_send(self.data["order_cancel"])

    '''
    正式发起派单请求
    '''
    def launch_dispatch(self):
        return self.api_send(self.data["launch_dispatch"])

    '''
    尝试发起派单请求
    '''
    def prepare_dispatch(self):
        pass


    '''
    支付流程中查询订单状态
    '''
    def order_payment_status(self):
        return self.api_send(self.data["order_payment_status"])

    '''
    订单确认页信息
    '''
    def order_info(self):
        return self.api_send(self.data["order_info"])

    def order_check(self):
        return self.api_send(self.data["order_check"])

    '''
    订单挂断时接口
    '''
    def report_event(self):
        pass
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
    def cancel_dispatch(self):
        return self.api_send(self.data["cancel_dispatch"])

    '''
    面诊师弹出卡片信息接口,去掉面诊时长/面诊人数/粉丝数 展示 显示 好评率/接通率 or 好评率/有效面诊
    '''
    def consultant(self):
        pass
    '''
    视频面诊工作台-首页
    '''
    def home(self):

        return self.api_send(self.data["home"])
    '''
    视频面诊工作台 - 待抢面诊派单 
    '''
    def current_dispatch_task_list(self):
        return self.api_send(self.data["current_dispatch_task_list"])

    '''
    视频面诊工作台 - 待抢面诊派单数量
    '''
    def current_dispatch_task_count(self):
        return self.api_send(self.data["current_dispatch_task_count"])
    '''
    面诊报告列表
    '''
    def reports(self):
        return self.api_send(self.data["reports"])

    def consultant(self):
        pass




if __name__ == '__main__':
    Testapi()
    # Testapi().test_consultation_orders("2020", "04", "1")
    # Testapi().consultation_order_list()
    # Testapi().consultation_order_detail()
    # Testapi().order_payment()
    # Testapi().order_cancel()
    # Testapi().launch_dispatch()
    # Testapi().order_payment_status()
    # Testapi().order_info()
    # Testapi().order_check()
    # Testapi().prepare_one2one()


