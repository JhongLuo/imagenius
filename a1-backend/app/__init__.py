from flask import Flask
from .app_operations import init_app
import logging
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler

webapp = Flask(__name__)
CORS(webapp, resources={r"/*": {"origins": "*"}})

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('logfile.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


global stats
stats = init_app(None)

def start_scheduler(stats):
    scheduler = BackgroundScheduler()
    def syncStats(stats):
        stats.syncDB()
    scheduler.add_job(func=syncStats, trigger='interval', args=(stats,), seconds=5)
    scheduler.start()

start_scheduler(stats) 


from app import  main