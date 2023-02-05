from flask import Flask
from .app_operations import init_app
import logging
from flask_cors import CORS


webapp = Flask(__name__)
CORS(webapp, resources={r"/*": {"origins": "*"}})

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('logfile.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


global stats
global scheduler
stats, scheduler = init_app()

from app import  main