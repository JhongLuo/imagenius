from .cache import Cache
from . import db_operations, storage_operations
from .statistics import Statistics

def init_app(db=None, stats=None, memcache=None):
    if db:
        db.close()
    db = db_operations.init_db()
    if not stats:
        stats = Statistics()
    stats.add2db(db)
    memcache = Cache(stats)
    stats.memcache_updated(memcache)
    storage_operations.clear_images()
    return db, stats, memcache
    
    