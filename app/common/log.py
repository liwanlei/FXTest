# -*- coding: utf-8 -*-
# @Date    : 2017-07-20 12:51:06
# @Author  : lileilei 
import logging,time,os
class log_t():
	def __init__(self,title,filename):
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
import os
import logbook
from logbook.more import ColorizedStderrHandler
from functools import wraps
check_path='.'
LOG_DIR = os.path.join(check_path, 'log')
file_stream = False
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
    file_stream = True
def get_logger(name='jiekou', file_log=file_stream, level=''):
    """ get logger Factory function """
    logbook.set_datetime_format('local')

    ColorizedStderrHandler(bubble=False, level=level).push_thread()
    logbook.TimedRotatingFileHandler(
            os.path.join(LOG_DIR, '%s.log' % name),
            date_format='%Y-%m-%d-%H', bubble=True, encoding='utf-8').push_thread()
    return logbook.Logger(name)

LOG = get_logger(file_log=file_stream, level='INFO')
def logger(param):
    """ fcuntion from logger meta """
    def wrap(function):
        """ logger wrapper """
        @wraps(function)
        def _wrap(*args, **kwargs):
            """ wrap tool """
            LOG.info("当前模块 {}".format(param))
            # LOG.info("全部args参数参数信息 , {}".format(str(args)))
            # LOG.info("全部kwargs参数信息 , {}".format(str(kwargs)))
            return function(*args, **kwargs)
        return _wrap
    return wrap