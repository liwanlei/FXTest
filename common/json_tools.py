'''
  @Description  统一的 JSON 响应工具
  @author       leizi
'''
from flask import jsonify
from typing import Union


def response(*, code=1, data: Union[list, dict, str] = None, message="message"):
    """返回标准 JSON 响应。"""
    return jsonify({
        'code': code,
        'message': message,
        'data': data,
    })


# 向后兼容别名：历史代码中误拼为 reponse，保留以避免外部调用中断
reponse = response
