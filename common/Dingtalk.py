""" 
@author: lileilei
@file: Dingtalk.py 
@time: 2017/12/26 17:34 
"""
'''
封装钉钉群发消息,
用例钉钉的第三方的api，发送成功是返回True 失败返回False
'''
import requests, json


def send_ding(content: str, Dingtalk_access_token: str):
    try:
        url = Dingtalk_access_token
        pagrem = {
            "msgtype": "text",
            "text": {
                "content": content
            },
            "isAtAll": True
        }
        headers = {
            'Content-Type': 'application/json'
        }
        f = requests.post(url, data=json.dumps(pagrem), headers=headers)
        if f.status_code == 200:
            return True
        else:
            return False
    except:
        return False
