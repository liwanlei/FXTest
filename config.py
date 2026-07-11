# encoding: utf-8
"""
@author: lileilei
@file: config.py
@time: 2017/7/13 16:39
"""
from app.models import Permisson

'''配置文件，后台一些需要的配置需要在这里进行配置'''
import os
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, \
	ProcessPoolExecutor

jenkins_url = os.environ.get('JENKINS_URL', 'http://localhost:8080')
jenkins_user = os.environ.get('JENKINS_USER', 'liwanlei')
jenkins_password = os.environ.get('JENKINS_PASSWORD', '')
xitong_request_toke = os.environ.get('SYSTEM_REQUEST_TOKEN', 'Fetext_token_system')
Try_Num_Case = 5
Interface_Time_Out = 5000
redis_password = os.environ.get('REDIS_PASSWORD', '')
max_connec_redis = 10
test_fail_try_num = 3  # 测试用例测试重试次数
PageShow = 25  # 这里配置的就是每个页显示多少条数据
Dingtalk_access_token = os.environ.get('DINGTALK_ACCESS_TOKEN', '')
OneAdminCount = 10
Config_import = 100
save_duration = 24 * 60
redis_host = os.environ.get('REDIS_HOST', '127.0.0.1')
redis_port = int(os.environ.get('REDIS_PORT', '6379'))
task_redis_db = int(os.environ.get('TASK_REDIS_DB', '3'))
redis_save_result_db = int(os.environ.get('REDIS_SAVE_RESULT_DB', '2'))
jmeter_data_db = os.environ.get('JMETER_DATA_DB', 'test')
paln_run_url = os.environ.get('PLAN_RUN_URL', 'http://127.0.0.1:5000')

email_type = "online.com"  # 用于校验邮箱
roles = {'User': Permisson.DELETE | Permisson.EDIT | Permisson.ADD,
		 'Oneadmin': Permisson.DELETE | Permisson.EDIT | Permisson.ADD | Permisson.ONEADMIN,
		 'Administrator': Permisson.DELETE | Permisson.EDIT | Permisson.ADD | Permisson.ONEADMIN | Permisson.ADMIN
		 }
REDIS = {
	'host': redis_host,
	'port': redis_port,
	'db': task_redis_db
}
jobstores = {
	'redis': RedisJobStore(**REDIS),
}
executors = {
	'default': ThreadPoolExecutor(10),
	'processpool': ProcessPoolExecutor(5)
}


class BaseConfig(object):
	'''所有环境共享的配置基类'''
	basedir = os.path.abspath(os.path.dirname(__file__))
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.163.com')
	MAIL_PORT = int(os.environ.get('MAIL_PORT', '25'))
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')
	CSRF_ENABLED = True
	UPLOAD_FOLDER = '/upload'

	@staticmethod
	def init_app(app):
		pass


class dev(BaseConfig):  # 研发环境配置
	SECRET_KEY = os.environ.get('SECRET_KEY', 'BaSeQuie')
	SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BaseConfig.basedir,
														  "data.sqlite")
	DEBUG = True


class test(BaseConfig):  # 测试环境的配置
	SECRET_KEY = os.environ.get('SECRET_KEY', 'BaSeQuie')
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', "sqlite:///" + os.path.join(BaseConfig.basedir, "test.sqlite"))
	DEBUG = True


class produce(BaseConfig):  # 线上环境的配置
	SECRET_KEY = os.environ.get('SECRET_KEY', 'ProduceFXTest')
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', "sqlite:///" + os.path.join(BaseConfig.basedir, "produce.sqlite"))
	DEBUG = False


def lod():
    env = os.environ.get('FLASK_ENV', 'dev')
    if env == 'test':
        return test
    elif env == 'produce':
        return produce
    return dev


class Config(object):
	JOBS = []
	SCHEDULER_API_ENABLED = True
