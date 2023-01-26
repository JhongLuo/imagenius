from flask import Flask
from .cache import Cache

global memcache

webapp = Flask(__name__)
memcache = Cache()

from app import main