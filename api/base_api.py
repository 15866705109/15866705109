'''
公用的方法放到此处，例如json format,yaml文件加载等等
'''

import json
import os

import requests
import yaml


# from gm.api.api_face import Testapi
# from gm.api.base_api import Testapi
from gm.api import path_setting


class BaseApi:
    params = {}

    @classmethod
    def format(cls, r):
        cls.r = r
        # print(json.dumps(r.json(), indent=2))
        print(json.dumps(json.loads(r.text), indent=2, ensure_ascii=False))

    # 封装yaml文件读取
    @classmethod
    def yaml_load(cls, path) -> list:
        with open(path) as f:
            return yaml.safe_load(f)

    # 调用yaml加载文件API加载
    def api_load(self, path):
        return self.yaml_load(path)

    # @classmethod
    # def api_host(cls, path):
    #     host = cls.api_load(path)
    #     return host

    def get_cookie(self, req: dict):
        host = self.api_load(path_setting.HOSTYAML_CONFIG)
        r = requests.request(
            req['method'],
            url=host['merchant_host']['url']+req['url'],
            params=req['params'],
            headers=req['headers'],
            data=req['data'],
            json=req['json']
        )
        item = r.cookies.values()
        print("---------",item)

        if len(item) == 1:
            headers = '_gtid={}'.format(item[0])
            print("cookie异常")

        else:
            headers = '_gtid={};sessionid={}'.format(item[0], item[1])

        return headers

    def read_header(self):
        with open("../api/get_cookie.txt", 'r') as f:
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

        headers = self.read_header()
        r = requests.request(
            req['method'],
            url=host['merchant_host']['url'] + req['url'],
            params=req.get('params'),
            headers=headers,
            data=req.get('data'),
            json=req.get('json')
        )
        print("api_send", type(r))
        return r.json()


if __name__ == '__main__':
    BaseApi().api_load("../api/api.yaml")
