""" 
@author: lileilei
@file: parsenei.py 
@time: 2018/3/14 16:17 
"""
'''
mockserver封装,用于在提供mock服务的时候使用
内部在headers里面加个token校验，获取不到token默认为外部请求，
内部请求不会去校验headers，在系统内部的请求直接可以获取接口返回的参数。
'''
from flask import request, abort, jsonify, make_response
from app.models import *
from common.packagedict import comp_dict, dict_par
import json
from error_message import MessageEnum
from common.jsontools import reponse as jsonreponse
from common.systemlog import logger


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
        if token == 'Fetext_token_system':
            paerm = request.values.to_dict()
            if dict_par(paerm, huoqupath.params) == True:
                if huoqupath.rebacktype == 'json':
                    try:
                        json_fan = json.dumps(huoqupath.fanhui)
                        return jsonreponse(code=MessageEnum.successs.value[0],
                                           message=MessageEnum.successs.value[1],
                                           data=json_fan)
                    except Exception as e:
                        logger.exception(e)
                        return jsonreponse(code=MessageEnum.resquest_return_not_json.value[0],
                                           message=MessageEnum.resquest_return_not_json.value[1])
                else:
                    return jsonreponse(code=MessageEnum.request_method_not_support.value[0],
                                       message=MessageEnum.request_method_not_support.value[1])
            else:
                return jsonreponse(code=MessageEnum.method_parame_not_right.value[0],
                                   message=MessageEnum.method_parame_not_right.value[1])
    except Exception as e:
        logger.exception(e)
        if huoqupath.is_headers == True:
            if comp_dict(heders, huoqupath.headers) == True:
                if huoqupath.ischeck == True:
                    paerm = request.values.to_dict()
                    if dict_par(paerm, huoqupath.params) == True:
                        if huoqupath.rebacktype == 'json':
                            try:
                                json_return = json.dumps(huoqupath.fanhui)
                                return jsonreponse(code=MessageEnum.successs.value[0],
                                                   message=MessageEnum.successs.value[1],
                                                   data=json_return)
                            except Exception as e:
                                logger.exception(e)
                                return jsonreponse(code=MessageEnum.resquest_return_not_json.value[0],
                                                   message=MessageEnum.resquest_return_not_json.value[1])
                        elif huoqupath.rebacktype == 'xml':
                            response = make_response(huoqupath.fanhui)
                            response.content_type = 'application/xml'
                            return response
                        else:
                            return jsonreponse(code=MessageEnum.request_method_not_support.value[0],
                                               message=MessageEnum.request_method_not_support.value[1])
                    else:
                        return jsonreponse(code=MessageEnum.method_parame_not_right.value[0],
                                           message=MessageEnum.method_parame_not_right.value[1])
                else:
                    if huoqupath.rebacktype == 'json':
                        try:
                            json_return = json.dumps(huoqupath.fanhui)
                            return jsonreponse(code=MessageEnum.successs.value[0],
                                               message=MessageEnum.successs.value[1],
                                               data=json_return)
                        except Exception as e:
                            logger.exception(e)
                            return jsonreponse(code=MessageEnum.resquest_return_not_json.value[0],
                                               message=MessageEnum.resquest_return_not_json.value[1])
                    elif huoqupath.rebacktype == 'xml':
                        response = make_response(huoqupath.fanhui)
                        response.content_type = 'application/xml'
                        return response
                    return jsonreponse(code=MessageEnum.request_method_not_support.value[0],
                                       message=MessageEnum.request_method_not_support.value[1])
            return jsonreponse(code=MessageEnum.request_secure.value[0],
                               message=MessageEnum.request_secure.value[1])
        else:
            if huoqupath.ischeck == True:
                paerm = request.values.to_dict()
                if dict_par(paerm, huoqupath.params) == True:
                    if huoqupath.rebacktype == 'json':
                        try:
                            json_return = json.dumps(huoqupath.fanhui)
                            return jsonreponse(code=MessageEnum.successs.value[0],
                                               message=MessageEnum.successs.value[1],
                                               data=json_return)
                        except Exception as e:
                            logger.exception(e)
                            return jsonreponse(code=MessageEnum.resquest_return_not_json.value[0],
                                               message=MessageEnum.resquest_return_not_json.value[1])
                    elif huoqupath.rebacktype == 'xml':
                        response = make_response(huoqupath.fanhui)
                        response.content_type = 'application/xml'
                        return response
                    else:
                        return jsonreponse(code=MessageEnum.request_method_not_support.value[0],
                                           message=MessageEnum.request_method_not_support.value[1])
                return jsonreponse(code=MessageEnum.method_parame_not_right.value[0],
                                   message=MessageEnum.method_parame_not_right.value[1])
            if huoqupath.rebacktype == 'json':
                try:
                    json_return = json.dumps(huoqupath.fanhui)
                    return jsonreponse(code=MessageEnum.successs.value[0],
                                       message=MessageEnum.successs.value[1],
                                       data=json_return)
                except Exception as e:
                    logger.exception(e)
                    return jsonreponse(code=MessageEnum.resquest_return_not_json.value[0],
                                       message=MessageEnum.resquest_return_not_json.value[1])
            elif huoqupath.rebacktype == 'xml':
                response = make_response(huoqupath.fanhui)
                response.content_type = 'application/xml'
                return response
            else:
                return jsonreponse(code=MessageEnum.request_method_not_support.value[0],
                                   message=MessageEnum.request_method_not_support.value[1])
