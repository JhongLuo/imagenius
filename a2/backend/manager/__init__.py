from flask import Flask
from flask_cors import CORS
from manager.Manager import Manager
from apscheduler.schedulers.background import BackgroundScheduler

webapp = Flask(__name__)
CORS(webapp, resources={r"/*": {"origins": "*"}})

global man
man = Manager()

def start_scheduler(man):
    scheduler = BackgroundScheduler()
    def syncStats(man):
        man.record()
    scheduler.add_job(func=syncStats, args=(man,))
    scheduler.start()

start_scheduler(man)

from manager import main