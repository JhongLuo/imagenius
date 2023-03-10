from flask import Flask
from . import Cache
from apscheduler.schedulers.background import BackgroundScheduler
import time

def start_scheduler(memcache):
    def syncStats(memcache):
        memcache.syncDB()
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=syncStats, trigger='interval', args=(memcache,), seconds=5)
    scheduler.start()

webapp = Flask(__name__)

global memcache

memcache = Cache.Cache()
time.sleep(1)
start_scheduler(memcache)
time.sleep(1)

from memcache import main