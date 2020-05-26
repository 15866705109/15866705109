import pytest
from face_api_test.api.api_face import Testapi
from face_api_test.api.base_api import BaseApi
from face_api_test.database import db_manage

class Test_api:

    @classmethod
    def setup_class(cls):
        cls.login = Testapi().login()


    def test_recommend_counsellors(self):
        a = Testapi().recommend_counsellors()

        print(a,1111)

    def test_counsellors(self):
        a = Testapi().counsellors()
        print(a,1111)

    def test_block_info(self):
        a = Testapi().block_info()
        print(a)
    def test_customer(self):
        a = Testapi().customer()
        print(a)

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
        print(a)

