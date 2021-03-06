'''
公用的方法放到此处，例如json format,yaml文件加载等等
'''

import json
import os
import random
import string

import requests
import yaml


# from face_api_test.api.api_face import Testapi
# from face_api_test.api.base_api import Testapi
from jsonpath import jsonpath
from pymysql import OperationalError

from face_api_test.api import path_setting


class BaseApi:
    params = {}

    @classmethod
    def format(cls,r):
        cls.r = r
        print(json.dumps(json.loads(r.text), indent=2, ensure_ascii=False))

    # 封装yaml文件读取
    @classmethod
    def yaml_load(cls, path) -> list:
        with open(path, encoding='utf-8') as f:
            return yaml.safe_load(f)

    # 调用yaml加载文件API加载
    def api_load(self, path):
        return self.yaml_load(path)

    def jsonpath(self, path, r=None, **kwargs):
        if r is None:
            r = self.r.json()
        return jsonpath(r, path)

    def get_cookie(self, req: dict):

        host = self.api_load(path_setting.HOSTYAML_CONFIG)
        print(host)
        r = requests.request(
            req['method'],
            url=host['merchant_host']['url']+req['url'],
            params=req['params'],
            headers=req['headers'],
            data=req['data'],
            json=req['json']
        )
        dict={}
        for i in r.cookies:
            dict[i.name]=i.value
        headers = '_gtid={};sessionid={}'.format(dict["_gtid"], dict["sessionid"])
        # item = r.cookies.values()
        # print("ppppppp",item)
        # if len(item) == 1:
        #     headers = '_gtid={}'.format(item[0])
        #     print("cookie异常")
        #
        # else:
        #     headers = '_gtid={};sessionid={}'.format(item[0], item[1])
        #
        return headers



    def read_header(self):
        with open("../api/get_cookie.txt", 'r', encoding='utf-8') as f:
            cookies = f.read()
        headers = {"cookie": cookies}
        return headers

    # 接口请求的封装
    def api_send(self, req: dict):
        host = self.api_load(path_setting.HOSTYAML_CONFIG)
        raw = yaml.dump(req)  # 将一个python对象生成为yaml文档
        for key, value in self.params.items():
            raw = raw.replace(f"${{{key}}}", repr(value))
        req = yaml.safe_load(raw)

        print('------',req.get('headers'))
        hd = req.get('headers')
        if hd == None:
            user_headers = self.read_header()
        elif hd["Cookie"]:
            user_headers = req.get('headers')
        else:
            user_headers = self.read_header()
        r = requests.request(
            req['method'],
            url=host['merchant_host']['url'] + req['url'],
            params=req.get('params'),
            headers=user_headers,
            data=req.get('data'),
            json=req.get('json')
        )
        return r.json()

    #随机生成trace_id
    def trace_id(self):
        return ''.join(random.sample(string.ascii_lowercase + string.digits, 32))



if __name__ == '__main__':
    BaseApi().api_load("../api/api.yaml")
    #print(BaseApi().trace_id())
    BaseApi().read_header()
