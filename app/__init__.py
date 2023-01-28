from flask import Flask
from .app_operations import init_app
import logging

global db
global stats
global memcache

webapp = Flask(__name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('logfile.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


db, stats, memcache = init_app()

from app import  main