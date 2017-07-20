# -*- coding: utf-8 -*-
# @Date    : 2017-07-20 12:51:06
# @Author  : lileilei 
import logging,time,os
class log_t():
	def __init__(self,title):
		self.day=time.strftime("%Y%m%d%H%M", time.localtime(time.time()))
		self.logger=logging.Logger(title)
		self.logger.setLevel(logging.INFO)
		basedir = os.path.abspath(os.path.dirname(__file__))
    	file_dir=os.path.join(basedir,'upload')
    	file=os.path.join(file_dir,self.day+'.log')
    	if os.path.exists(file) is False:
    		os.system('touch %s'%file)
    	self.logfile = logging.FileHandler(file)
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