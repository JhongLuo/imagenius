from flask import Flask
from .cache import Cache
from . import db_operations
from .statistics import Statistics

global memcache
global db
global stats
webapp = Flask(__name__)

db = db_operations.init_db()
stats = Statistics()
stats.add2db(db)
memcache = Cache(stats)

from app import  main