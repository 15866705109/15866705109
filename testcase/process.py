'''1V1和派单流程封装'''
from face_api_test.api import path_setting
from face_api_test.api.api_face import Testapi
from face_api_test.api.base_api import BaseApi


class Process:
    data = BaseApi().api_load(path_setting.PROCESS_DATA)
    param = data["per_lan_envent"]

    def per_lan_envent(self):
        r = Testapi().prepare_one2one(self.param["user_gender"], self.param["user_age"], self.param["counsellor_id"],
                                      self.param["referer"],
                                      self.param["user_has_aesthetic_medicine"], self.param["user_target_project"])
        print(r)
if __name__ == '__main__':
    Process().per_lan_envent()