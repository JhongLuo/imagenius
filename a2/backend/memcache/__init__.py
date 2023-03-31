from flask import Flask
from flask_cors import CORS
from . import Cache
from apscheduler.schedulers.background import BackgroundScheduler
import time
import datetime
def start_scheduler(memcache):
    def syncStats(memcache):
        last_sync_time = datetime.datetime.utcnow()
        while True:
            if datetime.datetime.utcnow() - last_sync_time > datetime.timedelta(seconds=5):
                print("syncing...")
                memcache.syncDB()
                last_sync_time = datetime.datetime.utcnow()
                print("synced")
            time.sleep(1)
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=syncStats, args=(memcache,))
    scheduler.start()

webapp = Flask(__name__)
CORS(webapp, resources={r"/*": {"origins": "*"}})
global memcache

memcache = Cache.Cache()
time.sleep(1)
start_scheduler(memcache)
time.sleep(1)

from memcache import main