'''
  @Description      
  @auther         leizi
'''
import os
import time
from loguru import logger

log_path = os.path.join(os.getcwd(), 'logs')
if not os.path.exists(log_path):
    os.mkdir(log_path)
log_path_error = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}_info.log')
logger.add(log_path_error, rotation="12:00", retention="5 days", enqueue=True)