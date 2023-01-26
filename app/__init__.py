from flask import Flask
from .cache import Cache
from .db_operations import init_db
import mysql.connector

global memcache
global db
webapp = Flask(__name__)
memcache = Cache()
db = init_db()

from app import  main