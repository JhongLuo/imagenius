from flask import Flask
from flask_cors import CORS
from autoscaler.scaler import Scaler
from apscheduler.schedulers.background import BackgroundScheduler


webapp = Flask(__name__)
CORS(webapp, resources={r"/*": {"origins": "*"}})

global scaler

scaler = Scaler()

def start_scheduler(scaler):
    def run(scaler):
        scaler.run()
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=run, args=(scaler,))
    scheduler.start()

start_scheduler(scaler)

from autoscaler import main