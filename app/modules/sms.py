# -*- coding: utf-8 -*-

import requests
import hashlib
import time
import uuid
import random


class NeteaseSmsAPI(object):
    """ 网易云信短信验证码服务 API 接口:
    """
    APP_KEY = "511f46341f1c38f3074024d17382a473"
    APP_SECRET = "3b504ed87dd0"

    # 接口列表:
    API_URLS = {
        "send": "https://api.netease.im/sms/sendcode.action",
        "verify": "https://api.netease.im/sms/verifycode.action",
        "send_template": "https://api.netease.im/sms/sendtemplate.action",
        "query_status": "https://api.netease.im/sms/querystatus.action",
    }

    def __init__(self, app_key=None, app_secret=None):
        self.app_key = app_key or self.APP_KEY
        self.app_secret = app_secret or self.APP_SECRET
        self.urls = self.API_URLS

    @property
    def nonce(self):
        return uuid.uuid4().hex

    @property
    def curtime(self):
        return str(int(time.time()))

    def checksum(self, nonce, curtime):
        s = "{}{}{}".format(self.app_secret, nonce, curtime).encode(encoding="utf-8")
        return hashlib.sha1(s).hexdigest()

    @property
    def http_headers(self):
        """ 构造 HTTP 请求头

        :return:
        """
        nonce = self.nonce
        curtime = self.curtime
        checksum = self.checksum(nonce, curtime)

        return {
            "AppKey": self.app_key,
            "CurTime": curtime,
            "Nonce": nonce,
            "CheckSum": checksum,
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        }

    @property
    def random_code(self):
        """ 自定义生成6位验证码
        :return:
        """
        return str(random.randint(100000, 999999))

    @staticmethod
    def _post(url, data, headers):
        r = requests.post(url, data=data, headers=headers)
        print("url: {}\nHTTP-header: {}\nHTTP-data: {}".format(url, headers, data))
        print("\tstatus: {} \tresult: {}".format(r.status_code, r.content))
        return r.json() if r.status_code == 200 else {}

    def send_code(self, mobile):
        """ 调用网易短信验证码服务接口, 发送验证码到手机.
        :param mobile: 手机号
        :return: 返回调用结果
                - {'msg': '4', 'code': 200, 'obj': '4123'}
                - obj: 验证码内容
                - code: 状态码
                - msg: 对应 查询里的 send_id 参数
        """
        url = self.urls.get("send")
        data = {
            "mobile": str(mobile)
        }
        return self._post(url, data=data, headers=self.http_headers)

    def send_template(self, template_id, mobiles, params=None):
        """ 发送模板短信
        :param template_id: 模板 ID, 目前测试发现: 只支持通知类模板, 不支持验证码模板.
        :param mobiles: 手机号列表
        :param params: 参数列表
        :return:
        """
        url = self.urls.get("send_template")
        data = {
            "mobiles": str([mobiles]) if not isinstance(mobiles, list) else mobiles
        }

        if template_id:
            data.update({"templateid": str(template_id)})

        if params:
            params = [params] if not isinstance(params, list) else params
            data.update({"params": str(params)})

        return self._post(url, data=data, headers=self.http_headers)

    def verify_code(self, mobile, code):
        """验证码正确性检查:
            - 只支持常规的验证码检查, 不支持模板验证码检查.
        :param mobile: 手机号
        :param code: 验证码, 对应 send_code() 返回值的 obj 字段
        :return:
        """
        url = self.urls.get("verify")
        data = {
            "mobile": str(mobile),
            "code": str(code)
        }
        return self._post(url, data=data, headers=self.http_headers)

    def query_status(self, send_id):
        """验证码发送状态查询:
            - 支持常规验证码检查, 同时也支持模板验证码检查.
        :param send_id: 发送 ID, 对应 send_code() 返回值的 msg 字段
        :return:
        """
        url = self.urls.get("query_status")
        data = {
            "sendid": str(send_id)
        }
        return self._post(url, data=data, headers=self.http_headers)

