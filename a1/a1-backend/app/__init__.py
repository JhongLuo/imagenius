from flask import Flask
import logging
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from utils.DBConnector import DBConnector
from . import storage_operations, memcache_operations
from .statistics import Statistics

webapp = Flask(__name__)
CORS(webapp, resources={r"/*": {"origins": "*"}})

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('logfile.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


global stats

memcache_operations.delete_keys()
DBConnector.delete_keys()
stats = Statistics()
stats.syncDB()
storage_operations.clear_images()

def start_scheduler(stats):
    scheduler = BackgroundScheduler()
    def syncStats(stats):
        stats.syncDB()
    scheduler.add_job(func=syncStats, trigger='interval', args=(stats,), seconds=5)
    scheduler.start()

start_scheduler(stats) 


from app import  main