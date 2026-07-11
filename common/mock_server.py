"""
@author: lileilei
@file: mock_server.py
@time: 2018/3/14 16:17
"""
'''
mockserver封装,用于在提供mock服务的时候使用
内部在headers里面加个token校验，获取不到token默认为外部请求，
内部请求不会去校验headers，在系统内部的请求直接可以获取接口返回的参数。
'''
import os
from flask import request, abort, jsonify, make_response
from app.models import *
from common.dict_utils import comp_dict, compare_dict_keys
import json
from error_message import MessageEnum
from common.json_tools import response as jsonreponse
from common.system_log import logger


SYSTEM_TOKEN = os.environ.get('SYSTEM_REQUEST_TOKEN', 'Fetext_token_system')


def _make_success_response(mock_config):
    """根据 mock 配置返回对应格式的响应。"""
    if mock_config.rebacktype == 'json':
        try:
            return jsonreponse(code=MessageEnum.success.value[0],
                               message=MessageEnum.success.value[1],
                               data=json.dumps(mock_config.fanhui))
        except Exception as e:
            logger.exception(e)
            return jsonreponse(code=MessageEnum.request_return_not_json.value[0],
                               message=MessageEnum.request_return_not_json.value[1])
    if mock_config.rebacktype == 'xml':
        response = make_response(mock_config.fanhui)
        response.content_type = 'application/xml'
        return response
    return jsonreponse(code=MessageEnum.request_method_not_support.value[0],
                       message=MessageEnum.request_method_not_support.value[1])


def _params_match(mock_config):
    """校验请求参数是否符合 mock 配置。"""
    paerm = request.values.to_dict()
    if compare_dict_keys(paerm, mock_config.params) is True:
        return True
    return False


def get_token_data(path):
    huoqupath = Mockserver.query.filter_by(path=path, status=True).first()
    if not huoqupath:
        abort(404)
    heders = request.headers
    method = request.method
    if method.lower() != huoqupath.methods:
        return jsonreponse(code=MessageEnum.request_method.value[0],
                           message=MessageEnum.request_method.value[1])

    try:
        token = heders['token']
    except Exception as e:
        logger.exception(e)
        token = None

    # 内部请求：token 校验通过，直接返回结果
    if token == SYSTEM_TOKEN:
        if not _params_match(huoqupath):
            return jsonreponse(code=MessageEnum.method_parame_not_right.value[0],
                               message=MessageEnum.method_parame_not_right.value[1])
        return _make_success_response(huoqupath)

    # 外部请求：根据是否需要 headers / params 校验决定流程
    if huoqupath.is_headers is True:
        if comp_dict(heders, huoqupath.headers) is not True:
            return jsonreponse(code=MessageEnum.request_secure.value[0],
                               message=MessageEnum.request_secure.value[1])
        if huoqupath.ischeck is True and not _params_match(huoqupath):
            return jsonreponse(code=MessageEnum.method_parame_not_right.value[0],
                               message=MessageEnum.method_parame_not_right.value[1])
        return _make_success_response(huoqupath)

    # 不需要 headers 校验
    if huoqupath.ischeck is True:
        if not _params_match(huoqupath):
            return jsonreponse(code=MessageEnum.method_parame_not_right.value[0],
                               message=MessageEnum.method_parame_not_right.value[1])
    return _make_success_response(huoqupath)
