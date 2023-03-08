from flask import Flask
from . import Cache
import logging
from apscheduler.schedulers.background import BackgroundScheduler
import time

def start_scheduler(memcache):
    def syncStats(memcache):
        memcache.syncDB()
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=syncStats, trigger='interval', args=(memcache,), seconds=5)
    scheduler.start()

webapp = Flask(__name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('logfile.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

global memcache
memcache = Cache.Cache()
time.sleep(1)
start_scheduler(memcache)


from memcache import main