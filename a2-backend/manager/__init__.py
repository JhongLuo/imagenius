from flask import Flask
from flask_cors import CORS
from manager.Manager import Manager

webapp = Flask(__name__)
CORS(webapp, resources={r"/*": {"origins": "*"}})

global man

man = Manager()

from manager import main