
import os, sys
import logging
from logging.handlers import RotatingFileHandler

def initLogging():
    if os.path.exists('./log') == False:
        os.mkdir("./log")

    logger = logging.getLogger()    #get root logger
    logger.setLevel(logging.INFO)    
    
    log_max_size = 20 * 1024 * 1024
    log_file_count = 20
    fileHandler = RotatingFileHandler(filename='./log/preprocessor.log', encoding='utf-8', maxBytes=log_max_size, backupCount=log_file_count)

    formatter = logging.Formatter('[%(levelname)s] %(asctime)s %(filename)s:%(lineno)d - %(message)s')
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)