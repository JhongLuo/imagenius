from .cache import Cache
from . import DBConnector, storage_operations
from .statistics import Statistics
from apscheduler.schedulers.background import BackgroundScheduler

def start_scheduler(db, stats, memcache):
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=syncStats, trigger='interval', args=(db, stats, memcache), seconds=5)
    scheduler.start()
    return scheduler

def syncStats(db, stats, memcache):
    stats.set2db(db)
    memcache.set_config(stats)

def init_app(db=None, stats=None, memcache=None, scheduler=None):
    if scheduler and scheduler.running:
        scheduler.remove_all_jobs()
        scheduler.shutdown()
    if db:
        db.close()
    db = DBConnector.DBConnector()
    if not stats:
        stats = Statistics()
    stats.add2db(db)
    memcache = Cache(stats)
    stats.memcache_updated(memcache)
    storage_operations.clear_images()
    scheduler = start_scheduler(db, stats, memcache)
    return db, stats, memcache, scheduler
    
    