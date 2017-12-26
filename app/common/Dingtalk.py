""" 
@author: lileilei
@license: Apache Licence  
@file: Dingtalk.py 
@time: 2017/12/26 17:34 
"""
import  requests,json
from  config import Dingtalk_access_token
def send_ding(content):
    url = 'https://oapi.dingtalk.com/robot/send?access_token=301a646888fb8e3f169461049851b36b89be1d16cf25a7c77593156c67f5e5db'
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
    if f.status_code==200:
        return True
    else:
        return False