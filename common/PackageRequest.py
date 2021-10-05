# -*- coding: utf-8 -*-
# @Date    : 2017-07-20 15:13:25
# @Author  : lileilei
'''
requets模块的简单的封装
'''
import requests, json
from config import Interface_Time_Out
from requests import exceptions
from common.systemlog import logger

class reques():
    def get(self, url, headers, parms):  # get消息
        try:
            self.r = requests.get(url, headers=headers, params=parms, timeout=Interface_Time_Out)
            self.r.encoding = 'UTF-8'
            spend = self.r.elapsed.total_seconds()
            json_response = json.loads(self.r.text)
            return json_response, spend
        except exceptions.Timeout:
            logger.exception(exceptions.Timeout)
            return {'get请求出错': "请求超时"}
        except exceptions.InvalidURL:
            logger.exception(exceptions.InvalidURL)
            return {'get请求出错': "非法url"}
        except exceptions.HTTPError:
            logger.exception(exceptions.HTTPError)
            return {'get请求出错': "http请求错误"}
        except Exception as e:
            logger.exception(e)
            return {'get请求出错': "错误原因:%s" % e}

    def post(self, url, params, headers):  # post消息
        data = json.dumps(params)
        try:
            reponse = requests.post(url,
                                    data=data,
                                    timeout=Interface_Time_Out,
                                    headers=headers)

            if reponse.status_code != 200:
                return {'post请求出错': "状态码返回不是200"}
            json_response = json.loads(reponse.text)
            spend = reponse.elapsed.total_seconds()
            return json_response, spend
        except exceptions.Timeout:
            logger.info(exceptions.Timeout)
            return {'post请求出错': "请求超时"}
        except exceptions.InvalidURL:
            logger.info(exceptions.InvalidURL)
            return {'post请求出错': "非法url"}
        except exceptions.HTTPError:
            logger.info(exceptions.HTTPError)
            return {'post请求出错': "http请求错误"}
        except Exception as e:
            logger.info(e)
            return {'post请求出错': "错误原因:%s" % e}
    def put(self, url, params, headers):  # post消息
        data = json.dumps(params)
        try:
            reponse = requests.put(url,
                                    data=data,
                                    timeout=Interface_Time_Out,
                                    headers=headers)

            if reponse.status_code != 200:
                logger.info(reponse.status_code)
                return {'put请求出错': "状态码返回不是200"}
            json_response = json.loads(reponse.text)
            spend = reponse.elapsed.total_seconds()
            return json_response, spend
        except exceptions.Timeout:
            logger.info(exceptions.Timeout)
            return {'put请求出错': "请求超时"}
        except exceptions.InvalidURL:
            logger.info(exceptions.InvalidURL)
            return {'put请求出错': "非法url"}
        except exceptions.HTTPError:
            logger.info(exceptions.HTTPError)
            return {'put请求出错': "http请求错误"}
        except Exception as e:
            logger.info(e)
            return {'put请求出错': "错误原因:%s" % e}


    def delfile(self, url, params, headers):  # 删除的请求
        try:
            self.rdel_word = requests.delete(url, data=params,
                                             headers=headers,
                                             timeout=Interface_Time_Out)
            json_response = json.loads(self.rdel_word.text)
            spend = self.rdel_word.elapsed.total_seconds()
            return json_response, spend
        except exceptions.Timeout:
            logger.info(exceptions.Timeout)
            return {'delete请求出错': "请求超时"}
        except exceptions.InvalidURL:
            logger.info(exceptions.InvalidURL)
            return {'delete请求出错': "非法url"}
        except exceptions.HTTPError:
            logger.info(exceptions.HTTPError)
            return {'delete请求出错': "http请求错误"}
        except Exception as e:
            logger.info(e)
            return {'delete请求出错': "错误原因:%s" % e}

    def putfile(self, url, params, headers):  # put请求
        try:
            self.rdata = json.dumps(params)
            me = requests.put(url, self.rdata, headers=headers,
                              timeout=Interface_Time_Out)
            json_response = json.loads(me.text)
            spend = me.elapsed.total_seconds()
            return json_response, spend
        except exceptions.Timeout:
            logger.exception(exceptions.Timeout)
            return {'put请求出错': "请求超时"}
        except exceptions.InvalidURL:
            logger.exception(exceptions.InvalidURL)
            return {'put请求出错': "非法url"}
        except exceptions.HTTPError:
            logger.exception(exceptions.HTTPError)
            return {'put请求出错': "http请求错误"}
        except Exception as e:
            logger.exception(e)
            return {'put请求出错': "错误原因:%s" % e}
