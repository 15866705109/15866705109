"""
 1V1和派单通用流程封装
"""

import time

from face_api_test.api import path_setting
from face_api_test.api.api_face import Testapi
from face_api_test.api.base_api import BaseApi


class Process:

    # 针对连线发起心跳流程抽离
    @classmethod
    def event_order_check(self, consultation_record_id, param, event_id, order_no):
        count = 1
        while count < 30:
            Testapi().report_event('', '', 8, consultation_record_id, param["device_id_lanch"])
            time.sleep(3)
            Testapi().report_event(param["user_agent"], param["cookie"], 8,
                                   consultation_record_id, param["device_id_recive"])
            time.sleep(1)
            count += 1
        Testapi().report_event('', '', event_id, consultation_record_id, param["device_id_lanch"])
        Testapi().order_info(order_no)
        r = Testapi().order_check(order_no)
        print(r)

    # 1V1发起视频通用功能抽离
    @classmethod
    def prepare_op(self, param):
        r = Testapi().prepare_one2one(param["user_gender"], param["user_age"], param["counsellor_id"], param["referer"],
                                      param["user_has_aesthetic_medicine"], param["user_target_project"])
        consultation_record_id = ''
        if r["error"] == 0:
            order_no = r["data"]["order_no"]
            trace_id = BaseApi().trace_id()
            lan_r = Testapi().launch_one2one(trace_id, order_no)
            consultation_record_id = lan_r["data"]["consultation_record_id"]
        return (consultation_record_id, order_no)

    # 派单通用请求抽离
    @classmethod
    def dispatch_op(self, param):
        trace_id = Testapi().trace_id()
        r = Testapi().prepare_dispatch(param["user_gender"], param["user_age"], param["referer"],
                                      param["user_has_aesthetic_medicine"], param["user_target_project"],
                                      param["counsellor_id"], param["counsellor_type"])
        print('你猜吧',r)
        dispatch_task_id = ""
        if r["error"] == 1:
            print("用户存在未结束的通话")
        else:
            order_no = r["data"]["order_no"]
            Testapi().launch_dispatch(order_no, trace_id)
            print('你猜',Testapi().launch_dispatch(order_no, trace_id))
            count = 1
            while count < 5:
                Testapi().current_dispatch_ping()    #发请求
                print('不知道是啥',Testapi().current_dispatch_ping())
                time.sleep(1)

                r = Testapi().current_dispatch_task_list()
                print('yuchao',r)
                if r["data"] != []:
                    dispatch_task_id = r["data"][0]["dispatch_task_id"]
                    break
                count += 1

            # 医生加入抢单
            Testapi().join_dispatch(param["cookie"], dispatch_task_id)
            print('dispatch_task_id是',Testapi().join_dispatch(param["cookie"], dispatch_task_id))
            # 用户获取派单信息
            result = Testapi().get_current_dispatch_info()
            print('获取派单',result)
            consultation_record_id = result["data"]["consultation_record_info"]
        return (consultation_record_id,order_no, dispatch_task_id)



    # 发起视频面诊到用户侧report_event
    # def per_lan_envent(self):
    #     consultation_record_id, order_no = self.prepare_op(self.param_normal_process)
    #     # r = Testapi().prepare_one2one(self.param["user_gender"], self.param["user_age"], self.param["counsellor_id"],
    #     #                               self.param["referer"],
    #     #                               self.param["user_has_aesthetic_medicine"], self.param["user_target_project"])
    #     # if r["error"] == 0:
    #     #     order_no = r["data"]["order_no"]
    #     #     trace_id = BaseApi().trace_id()
    #     #     lan_r = Testapi().launch_one2one(trace_id, order_no)
    #     #     consultation_record_id = lan_r["data"]["consultation_record_id"]
    #         Testapi().report_event(2, consultation_record_id)
    #         print(r)
    #     else:
    #         print("视频面诊异常")

    # 用户方发起1V1视频面诊接通后，用户测取消情况
    def cancel_perone(self):
        pass
        # consultation_record_id, order_no = self.prepare_op(self.param_cancel)
        # if consultation_record_id != '':
        #     Testapi().report_event("", "", 2, consultation_record_id)
        #     count = 1
        #     while count < 10:
        #         Testapi().report_event(8, consultation_record_id)
        #         time.sleep(1)
        #         count += 1
        #     Testapi().report_event(6, consultation_record_id)
        # else:
        #     print("视频面诊异常")

    # 1v1面诊用户加入失败情况
    def user_join_failed(self):
        consultation_record_id = self.prepare_op(self.param_join_failed)
        if consultation_record_id != '':
            Testapi().report_event(3, consultation_record_id)
        else:
            print("视频面诊异常")

    # 模拟派单请求
    def launch_disp(self):
        consultation_record_id, order_no, dispatch_task_id = self.dispatch_op(self.param_launch_disp)
        # 医生加入
        Testapi().report_event(self.param_normal_process["user_agent"], self.param_normal_process["cookie"], 2,
                               consultation_record_id, self.param_normal_process["device_id_recive"])
        # 用户加入
        Testapi().report_event("", "", 2, consultation_record_id, self.param_normal_process["device_id_recive"])
        self.event_order_check(consultation_record_id, self.param_normal_process, 7, order_no)


if __name__ == '__main__':
    # Process().per_lan_envent()
    # Process().cancel_perone()
    Process().launch_disp()
    # Process().normal_process()
