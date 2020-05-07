import configparser

from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])
import common.config.appconfig as appconfig
import common.utils.ExceptionUtil as exUtil

class Config:
    def init(self, server):
        try:
            config = configparser.ConfigParser()
            config.read(f'./config_{server}.ini', encoding='utf-8')            

            appconfig.dbhost = config['MYSQL']['host']
            appconfig.dbname = config['MYSQL']['dbname']
            appconfig.dbuser = config['MYSQL']['user']
            appconfig.dbpassword = config['MYSQL']['password']
            appconfig.dbport = config['MYSQL']['port']

            appconfig.redis_host_port = config['REDIS']['host_port']
            appconfig.redis_master = config['REDIS']['master']
            appconfig.redis_password = config['REDIS']['password']

            appconfig.kafka_bootstrap_servers = config['KAFKA']['bootstrap_servers']
            appconfig.kafka_topics = config['KAFKA']['topics']
            appconfig.kafka_group_id = config['KAFKA']['group_id']
            appconfig.kafka_consumer_timeout_ms = config['KAFKA']['consumer_timeout_ms']
            appconfig.kafka_auto_offset_reset = config['KAFKA']['auto_offset_reset']
            
            appconfig.upload_path = config['FILEPATH']['upload_path']
            appconfig.scrap_path = config['FILEPATH']['scrap_path']
            appconfig.crop_path = config['FILEPATH']['crop_path']
            appconfig.thumb_path = config['FILEPATH']['thumb_path']
        except Exception as ex:
            exUtil.printException()
            raise Exception(f'check your parameters: {server}')
