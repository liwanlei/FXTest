from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime,timedelta
import logging

sched = BlockingScheduler()
def my_job():
    print ('my_job is running, Now is %s' % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

#添加作业
sched.add_job(my_job,'interval',id='myjob',seconds=5)

log = logging.getLogger('apscheduler.executors.default')
log.setLevel(logging.INFO)  # DEBUG
#设定日志格式
fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
h = logging.StreamHandler()
h.setFormatter(fmt)
log.addHandler(h)

sched.start()