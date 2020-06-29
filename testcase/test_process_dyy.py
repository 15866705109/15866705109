import time

import pytest

from face_api_test.api import path_setting
from face_api_test.api.api_face import Testapi
from face_api_test.api.base_api import BaseApi
from face_api_test.testcase.ids_list import get_ids
from face_api_test.testcase.process import Process



class TestProcess:
    data = BaseApi().api_load(path_setting.PROCESS_DATA)
    normal_process_case, normal_process_data = get_ids(data, 'normal_process')
    # param = data["per_lan_envent"]
    cancel_perone_case, cancel_perone_data = get_ids(data, 'cancel_perone')
    join_failed_case, join_failed_data = get_ids(data, 'join_failed')
    launch_disp_case, launch_disp_data = get_ids(data, 'launch_disp')

    # 正常接听流程,用户主动退出
    @pytest.mark.parametrize("param", normal_process_data, ids=normal_process_case)
    def test_normal_process(self, param):
        consultation_record_id, order_no = Process().prepare_op(param)
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

            result = Process().event_order_check(consultation_record_id, param, 7, order_no)
            assert result["data"]["info"] == "success"
            print("测试通过")
        else:
            print("视频面诊异常")

    # 模拟派单请求
    @pytest.mark.parametrize("param", launch_disp_data, ids=launch_disp_case)
    def test_launch_disp(self, param):
        consultation_record_id, order_no, dispatch_task_id = Process().dispatch_op(param)
        # 医生加入
        Testapi().report_event(param["user_agent"], param["cookie"], 8,
                               consultation_record_id, param["device_id_lanch"])
        # 用户加入
        Testapi().report_event("", "", 2, consultation_record_id, param["device_id_recive"])
        result = Process().event_order_check(consultation_record_id, param, 7, order_no)
        assert result["data"]["info"] == "success"

    # 用户方发起1V1，医生接通前，用户测取消情况
    @pytest.mark.parametrize("param", cancel_perone_data, ids=cancel_perone_case)
    def test_cancel_perone(self, param):
        consultation_record_id, order_no = Process().prepare_op(param)
        if consultation_record_id != '':
            Testapi().report_event("", "", 2, consultation_record_id)
            # count = 1
            # while count < 10:
            #     Testapi().report_event(8, consultation_record_id)
            #     time.sleep(1)
            #     count += 1
            result = Testapi().report_event('', '', 6, consultation_record_id)
            assert result["data"]["status"] == param["status"]
            assert result["data"]["finish_reason"] == param["finish_reason"]
        else:
            print("视频面诊异常")


    # 1v1面诊用户加入失败情况
    @pytest.mark.parametrize("param", join_failed_data, ids=join_failed_case)
    def test_user_join_failed(self, param):
        consultation_record_id, order_no = Process().prepare_op(param)
        if consultation_record_id != '':
            result = Testapi().report_event('', '', 3, consultation_record_id)
            assert result["data"]["status"] == param["status"]
            assert result["data"]["finish_reason"] == param["finish_reason"]
        else:
            print("视频面诊异常")