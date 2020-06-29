import pytest

from face_api_test.api import path_setting
from face_api_test.api.api_face import Testapi
from face_api_test.api.base_api import BaseApi
from face_api_test.testcase.ids_list import get_ids
from face_api_test.testcase.process import Process


class TestProcess:
    data = BaseApi().api_load(path_setting.PROCESS_DATA)
    normal_process_case, normal_process_data = get_ids(data, 'normal_process')
    # param = data["per_lan_envent"]:
    # param_cancel = data['cancel_perone']
    # param_join_failed = data['join_failed']
    # param_normal_process = data['normal_process']
    # param_launch_disp = data['launch_disp']

    # 正常接听流程,用户主动退出
    @pytest.mark.parametrize("param", normal_process_data, ids=normal_process_case)
    def test_normal_process(self, param):
        consultation_record_id, order_no = Process().prepare_op(param)
        print(order_no,1111)
        if consultation_record_id != "":
            Testapi().get_consultation_record(param["cookie"], consultation_record_id)
            # 用户加入成功
            Testapi().report_event('', '', 2, consultation_record_id, param["device_id_recive"])
            # 医生接受邀请
            Testapi().report_event(param["user_agent"], param["cookie"], 4,
                                   consultation_record_id, param["device_id_recive"])
            # 医生加入成功
            Testapi().report_event(param["user_agent"], param["cookie"], 2,
                                   consultation_record_id, param["device_id_lanch"])

            Process().event_order_check(consultation_record_id, param, 7, order_no)
            print("测试通过")
        else:
            print("视频面诊异常")


