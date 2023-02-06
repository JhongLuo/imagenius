from utils.DBConnector import DBConnector
from . import storage_operations, memcache_operations
from .statistics import Statistics
from apscheduler.schedulers.background import BackgroundScheduler

def start_scheduler(stats):
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=syncStats, trigger='interval', args=(stats,), seconds=5)
    scheduler.start()
    return scheduler

def syncStats(stats):
    stats.syncDB()
    
def init_app(stats=None):
    memcache_operations.delete_keys()
    DBConnector.delete_keys()
    stats = Statistics()
    stats.syncDB()
    storage_operations.clear_images()
    return stats
    
    