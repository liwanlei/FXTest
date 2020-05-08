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


def get_to_data(path):
    huoqupath = Mockserver.query.filter_by(path=path, status=True).first()
    if not huoqupath:
        abort(404)
    heders = request.headers
    method = request.method
    if method.lower() != huoqupath.methods:
        return jsonify({'code': '-1', 'message': u'请求方式错误!', 'data': ''})
    try:
        token = heders['token']
        if token == 'Fetext_token_system':
            paerm = request.values.to_dict()
            if dict_par(paerm, huoqupath.params) == True:
                if huoqupath.rebacktype == 'json':
                    try:
                        json_fan = json.dumps(huoqupath.fanhui)
                        return jsonify({'code': '1', 'message': 'successs', 'data': json_fan})
                    except:
                        return jsonify({'code': '-2', 'message': u'你写入的返回不能正常json！请检查', 'data': ''})
                else:
                    return jsonify({'code': '-2', 'message': u'你写入的类型目前系统不支持', 'data': ''})
            else:
                return jsonify({'code': '-4', 'message': u'你输入的参数不正确', 'data': ''})
    except:
        if huoqupath.is_headers == True:
            if comp_dict(heders, huoqupath.headers) == True:
                if huoqupath.ischeck == True:
                    paerm = request.values.to_dict()
                    if dict_par(paerm, huoqupath.params) == True:
                        if huoqupath.rebacktype == 'json':
                            try:
                                json_fan = json.dumps(huoqupath.fanhui)
                                return jsonify({'code': '1', 'message': 'successs', 'data': json_fan})
                            except:
                                return jsonify({'code': '-2', 'message': u'你写入的返回不能正常json！请检查', 'data': ''})
                        elif huoqupath.rebacktype == 'xml':
                            response = make_response(huoqupath.fanhui)
                            response.content_type = 'application/xml'
                            return response
                        else:
                            return jsonify({'code': '-2', 'message': u'你写入的类型目前系统不支持', 'data': ''})
                    else:
                        return jsonify({'code': '-4', 'message': u'你输入的参数不正确', 'data': ''})
                else:
                    if huoqupath.rebacktype == 'json':
                        try:
                            json_fan = json.dumps(huoqupath.fanhui)
                            return jsonify({'code': '1', 'message': 'successs', 'data': json_fan})
                        except:
                            return jsonify({'code': '-2', 'message': u'你写入的返回不能正常json！请检查', 'data': ''})
                    elif huoqupath.rebacktype == 'xml':
                        response = make_response(huoqupath.fanhui)
                        response.content_type = 'application/xml'
                        return response
                    return jsonify({'code': '-2', 'message': u'你写入的类型目前系统不支持', 'data': ''})
            return jsonify({'code': '-3', 'message': u'安全校验失败!', 'data': ''})
        else:
            if huoqupath.ischeck == True:
                paerm = request.values.to_dict()
                if dict_par(paerm, huoqupath.params) == True:
                    if huoqupath.rebacktype == 'json':
                        try:
                            json_fan = json.dumps(huoqupath.fanhui)
                            return jsonify({'code': '1', 'message': 'successs', 'data': json_fan})
                        except:
                            return jsonify({'code': '-2', 'message': u'你写入的返回不能正常json！请检查', 'data': ''})
                    elif huoqupath.rebacktype == 'xml':
                        response = make_response(huoqupath.fanhui)
                        response.content_type = 'application/xml'
                        return response
                    else:
                        return jsonify({'code': '-2', 'message': u'你写入的类型目前系统不支持', 'data': ''})
                return jsonify({'code': '-4', 'message': u'你输入的参数不正确', 'data': ''})
            if huoqupath.rebacktype == 'json':
                try:
                    json_fan = json.dumps(huoqupath.fanhui)
                    return jsonify({'code': '1', 'message': 'successs', 'data': json_fan})
                except:
                    return jsonify({'code': '-2', 'message': u'你写入的返回不能正常json！请检查', 'data': ''})
            elif huoqupath.rebacktype == 'xml':
                response = make_response(huoqupath.fanhui)
                response.content_type = 'application/xml'
                return response
            else:
                return jsonify({'code': '-2', 'message': u'你写入的类型目前系统不支持', 'data': ''})
