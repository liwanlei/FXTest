'''
  @Description      
  @auther         leizi
'''
import os
from loguru import logger

log_path = os.path.join(os.path.join(os.getcwd(), 'app'),'upload')
def filelogpath(path):
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    log_path_error = os.path.join(log_path, path)
    logger.add(log_path_error)