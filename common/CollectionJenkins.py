'''
@author: lileilei
@file: CollectionJenkins.py
@time: 2018/8/17 9:45
'''
'''
jenkins的链接
'''
import jenkins, requests
from config import jenkins_password, jenkins_user, jenkins_url


class Conlenct_jenkins(object):
    def __init__(self):
        self.jenkins_password = jenkins_password
        self.jenkins_user = jenkins_user
        self.jenkins_url = jenkins_url
        try:
            self.servir = jenkins.Jenkins(url=self.jenkins_url, username=self.jenkins_user,
                                          password=self.jenkins_password, timeout=20)
        except Exception as e:
            print('Jenkins 链接失败!原因：%s' % e)

    def build_job(self, jobname):
        try:
            self.servir.build_job(jobname)
            return True
        except:
            return False

    def job_bulid_list(self, jobname):
        bulid_list = self.servir.get_job_info(jobname)['builds']
        return bulid_list

    def job_bulid_log(self, url, jobname):
        id = self.servir.get_job_info(jobname)['lastCompletedBuild']['number']
        url1 = url + str(id) + "/console"
        log = self.servir.jenkins_request(requests.Request('GET', url1)).text
        return log

    def last_build_result(self, id, jobname):
        result = self.servir.get_build_info(jobname, id)['result']
        return result

    def bulid_runing(self, id, jobname):
        runing = self.servir.get_build_info(jobname, id)['building']
        return runing

    def great_task(self, jobname, config_xml):
        try:
            self.servir.create_job(jobname, config_xml)
        except:
            print('创建构建失败')

    def rename_task(self, jobname, toname):
        try:
            self.servir.rename_job(jobname, toname)
        except:
            print('修改名字失败')

    def delete_task(self, jobname):
        self.servir.delete_job(jobname)

    def reconfig_job(self, jobname, config):
        self.servir.reconfig_job(jobname, config)

    def stop_build_job(self, jobname, id):
        self.servir.stop_build(jobname, id)

    def get_all_job(self):
        jobs = self.servir.get_all_jobs()
        return jobs
