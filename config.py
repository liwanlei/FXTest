# encoding: utf-8
"""
@author: lileilei
@file: config.py
@time: 2017/7/13 16:39
"""
'''配置文件，后台一些需要的配置需要在这里进行配置'''
import  os
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
jenkins_url='http://localhost:8080'#jenkins的地址
jenkins_user='liwanlei'#jenkins的用户名
jenkins_password='123456'#jenkins的密码
xitong_request_toke='Fetext_token_system'#系统内部依赖接口请求的时候需要加个token来区分
Try_Num_Case=5#重试的次数
Interface_Time_Out=5000#超时时间
jobstores = {
    'redis': RedisJobStore(),
}
executors = {
    'default': ThreadPoolExecutor(10),
    'processpool': ProcessPoolExecutor(3)
}
PageShow=25#这里配置的就是每个页显示多少条数据
Dingtalk_access_token=''#在这里配置您的接受通知的钉钉群自定义机器人webhook，
OneAdminCount=10 #设置项目管理员的数量
Config_daoru_xianzhi=50#配置可以导入限制
class dev(object):#研发环境配置
	SECRET_KEY = 'BaSeQuie'
	basedir=os.path.abspath(os.path.dirname(__file__))
	SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "data.sqlite")
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS=False
	CSRF_ENABLED = True
	UPLOAD_FOLDER='/upload'
	DEBUG = True
	@staticmethod
	def init_app(app):
		pass
class test(object):#测试环境的配置
	SECRET_KEY = 'BaSeQuie'
	basedir = os.path.abspath(os.path.dirname(__file__))
	SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "test.sqlite")
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	CSRF_ENABLED = True
	UPLOAD_FOLDER = '/upload'
	DEBUG = True

	@staticmethod
	def init_app(app):
		pass
class produce(object):#线上环境的配置
	SECRET_KEY = 'ProduceFXTest'
	basedir = os.path.abspath(os.path.dirname(__file__))
	SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "produce.sqlite")
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	CSRF_ENABLED = True
	UPLOAD_FOLDER = '/upload'
	DEBUG = True

	@staticmethod
	def init_app(app):
		pass
def lod():
	return dev
class Config(object):
	JOBS = [ ]
	SCHEDULER_API_ENABLED = True