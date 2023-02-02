from utils.DBConnector import DBConnector
from . import storage_operations, memcache_operations
from .statistics import Statistics
from apscheduler.schedulers.background import BackgroundScheduler

def start_scheduler(db, stats):
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=syncStats, trigger='interval', args=(db, stats), seconds=5)
    scheduler.start()
    return scheduler

def syncStats(db, stats):
    stats.syncDB(db)
    
def init_app(db=None, stats=None, scheduler=None):
    if scheduler and scheduler.running:
        scheduler.remove_all_jobs()
        scheduler.shutdown()
    if db:
        db.close()
    memcache_operations.delete_keys()
    db = DBConnector()
    db.delete_keys()
    if not stats:
        stats = Statistics()
    stats.syncDB(db)
    storage_operations.clear_images()
    scheduler = start_scheduler(db, stats)
    return db, stats, scheduler
    
    