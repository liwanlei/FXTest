# -*- coding: utf-8 -*-
# @Date    : 2017-07-20 12:51:06
# @Author  : lileilei
"""
日志模块，
这里会记录测试的日志。
"""
import logging


class log_t(object):
    def __init__(self, title, filename):
        self.logger = logging.Logger(title)
        self.logger.setLevel(logging.INFO)
        self.logfile = logging.FileHandler(filename)
        self.logfile.setLevel(logging.INFO)
        self.control = logging.StreamHandler()
        self.control.setLevel(logging.INFO)
        self.formater = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logfile.setFormatter(self.formater)
        self.control.setFormatter(self.formater)
        self.logger.addHandler(self.logfile)
        self.logger.addHandler(self.control)

    def debugInfo(self, message):
        self.logger.debug(message)

    def info_log(self, message):
        self.logger.info(message)

    def ware_log(self, message):
        self.logger.warn(message)

    def error_log(self, message):
        self.logger.error(message)
