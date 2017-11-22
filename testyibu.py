from flask import Flask
from flask_apscheduler import APScheduler
from flask import request
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
app = Flask(__name__)
scheduler = APScheduler()
import sqlite3
class Config(object):
    JOBS = [ ]
    SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(url='sqlite:///shebei.db')
    }
    SCHEDULER_EXECUTORS = {
        'processpool': ProcessPoolExecutor(4)
    }
    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False,
        'max_instances': 3
    }
    SCHEDULER_API_ENABLED = True

def job1(a, b):
    print(str(a) + ' ' + str(b))

def jobfromparm(jobargs):
    id = jobargs['id']
    func = jobargs['func']
    args = eval(jobargs['args'])
    trigger = jobargs['trigger']
    seconds = jobargs['seconds']
    print('add job: ',id)
    job = scheduler.add_job(func=job1,id=id, args=(1,2),trigger='interval',seconds=1,replace_existing=True)
    return 'sucess'

@app.route('/pause')
def pausejob(id):#暂停
    scheduler.pause_job(id)
    return "Success!"

@app.route('/resume')
def resumejob(id):#恢复
    scheduler.resume_job(id)
    return "Success!"
@app.route('/getjob')
def  get_jobs() :#获取
    jobs=scheduler.get_jobs()
    print(jobs)
    return '111'
def remove_job(id):#移除
    scheduler.resume_job(id)
    return 111
@app.route('/addjob', methods=['GET','POST'])
def addjob():
    data = request.values
    job = jobfromparm(data)
    return 'sucess'
#动态设置scheduler.reschedule_job('my_job_id', trigger='cron', minute='*/5')
#关闭所有scheduler.shutdown()
#sched.add_job(job_function, 'cron', day_of_week='mon-fri', hour=5, minute=30)
#周一到周五的早晨五点半执行
#@sched.scheduled_job('cron', day_of_week='mon-fri', hour='0-9', minute='30-59', second='*/3')
# def scheduled_job():
#     print('This job is run every weekday at 5pm.')

if __name__ == '__main__':
#    app = Flask(__name__)
    app.config.from_object('config')
    # it is also possible to enable the API directly
    # scheduler.api_enabled = True

    scheduler.init_app(app=app)
    scheduler.start()
    app.run(debug=True)
