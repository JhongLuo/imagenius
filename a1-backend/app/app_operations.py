from utils.DBConnector import DBConnector
from . import storage_operations, memcache_operations
from .statistics import Statistics



def init_app(stats):
    memcache_operations.delete_keys()
    DBConnector.delete_keys()
    stats = Statistics()
    stats.syncDB()
    storage_operations.clear_images()
    return stats
    
    