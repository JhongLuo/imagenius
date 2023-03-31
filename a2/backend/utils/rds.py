import mysql.connector
from utils.ReplacementPolicies import ReplacementPolicies
from enum import Enum
from utils.config import Config
import requests
class StatsNames(Enum):
    total_requests = "total_requests"
    read_requests = "read_requests"
    missed_requests = "missed_requests"
    replacement_policy = "replacement_policy"
    max_size = "max_size"
    
    
print(requests.get(Config.config_service_ip + '/rds'))
db_config = requests.get(Config.config_service_ip + '/rds').json()
print("config", db_config)


def cursor_operation(func):
    def wrapper(*args, **kwargs):
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        try:
            rtn = func(cursor, *args, **kwargs)
            conn.commit()
        except:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()
        return rtn
    return wrapper

# on the first run, create the database and tables

def create_database():
    new_config = db_config.copy()
    new_config.pop("database")
    conn = mysql.connector.connect(**new_config)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database']}")
    conn.commit()
    cursor.close()
    conn.close()
    
def init_database():
    create_database()
    delete_tables()
    create_tables()
    reset_tables()

def reset_tables():
    reset_stats()
    reset_memcache_status()
    reset_auto_scaler_status()
    delete_keys()

@cursor_operation
def delete_tables(cursor):
    cursor.execute("DROP TABLE IF EXISTS images")
    cursor.execute("DROP TABLE IF EXISTS stats")
    cursor.execute("DROP TABLE IF EXISTS memcache")

@cursor_operation
def create_tables(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS images (keyword VARCHAR(255) PRIMARY KEY, path VARCHAR(255) NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS stats (name VARCHAR(255) PRIMARY KEY, value DECIMAL(65, 3) NOT NULL)")
    # memcache has boolean status(default false) and int primary id
    cursor.execute("CREATE TABLE IF NOT EXISTS memcache (id INT PRIMARY KEY, is_started BOOLEAN DEFAULT FALSE)")

# memcache status operations

@cursor_operation
def reset_memcache_status(cursor, status=False):
    if status:
        status = "TRUE"
    else:
        status = "FALSE"
    for i in range(8):
        cursor.execute(f"INSERT INTO memcache (id, is_started) VALUES ({i}, {status}) ON DUPLICATE KEY UPDATE is_started = {status}")

@cursor_operation
def reset_auto_scaler_status(cursor, status=False):
    if status:
        status = "TRUE"
    else:
        status = "FALSE"
    cursor.execute(f"INSERT INTO memcache (id, is_started) VALUES ({8}, {status}) ON DUPLICATE KEY UPDATE is_started = {status}")

@cursor_operation
def get_memcache_status(cursor, id):
    if id >= 0 and id < 8:
        cursor.execute(f"SELECT is_started FROM memcache WHERE id = {id}")
        return bool(cursor.fetchone()[0])
    else:
        raise Exception("Invalid memcache id")

@cursor_operation
def get_online_memcache_nums(cursor):
    # id is from 0 to 7
    cursor.execute(f"SELECT COUNT(*) FROM memcache WHERE id < 8 AND is_started = TRUE")
    return cursor.fetchone()[0]

@cursor_operation
def set_memcache_status(cursor, id, status):
    if id >= 0 and id < 8:
        cursor.execute(f"UPDATE memcache SET is_started = {status} WHERE id = {id}")
    else:
        raise Exception("Invalid memcache id")

@cursor_operation
def set_autoscaler_status(cursor, status):
    cursor.execute(f"INSERT INTO memcache (id, is_started) VALUES (8, {status}) ON DUPLICATE KEY UPDATE is_started = {status}")
    
@cursor_operation
def get_autoscaler_status(cursor):
    cursor.execute(f"SELECT is_started FROM memcache WHERE id = 8")
    return bool(cursor.fetchone()[0])

# stats operations

@cursor_operation
def reset_stats(cursor):
    data = [
        (StatsNames.replacement_policy.value, ReplacementPolicies.LRU.value),
        (StatsNames.max_size.value, 100 * 1024 * 1024),
    ]
    for name, value in data:
        value = str(value)
        cursor.execute("INSERT INTO stats (name, value) VALUES (%s, %s) ON DUPLICATE KEY UPDATE value = %s", (name, value, value))

@cursor_operation
def get_replacement_policy(cursor):
    cursor.execute(f"SELECT value FROM stats WHERE name = '{StatsNames.replacement_policy.value}'")
    res = cursor.fetchone()
    return ReplacementPolicies.int2policy(res[0])

@cursor_operation
def set_replacement_policy(cursor, policy):
    cursor.execute(f"UPDATE stats SET value = {str(policy.value)} WHERE name = '{StatsNames.replacement_policy.value}'")

@cursor_operation
def get_stat(cursor, name : StatsNames):
    if name == StatsNames.max_size:
        cursor.execute(f"SELECT value FROM stats WHERE name = '{name.value}'")
        res = cursor.fetchone()
        return int(res[0])
    else:
        raise Exception("Cannot get this stat")

@cursor_operation
def set_stat(cursor, name : StatsNames, value):
    if name == StatsNames.max_size:
        cursor.execute(f"UPDATE stats SET value = {str(value)} WHERE name = '{name.value}'")
    else:
        raise Exception("Cannot set this stat")
    
# image operations

@cursor_operation
def delete_keys(cursor):
    cursor.execute("TRUNCATE TABLE images")

@cursor_operation
def get_keys(cursor):
    cursor.execute("SELECT keyword FROM images")
    res = cursor.fetchall()
    return [x[0] for x in res]

@cursor_operation
def set_key(cursor, keyword, path):
    cursor.execute("INSERT INTO images (keyword, path) VALUES (%s, %s) ON DUPLICATE KEY UPDATE path = %s", (keyword, path, path))
    
@cursor_operation
def delete_key(cursor, keyword):
    cursor.execute("DELETE FROM images WHERE keyword = %s", (keyword,))

@cursor_operation
def get_path(cursor, keyword):
    cursor.execute("SELECT path FROM images WHERE keyword = %s", (keyword,))
    res = cursor.fetchone()
    if res:
        return res[0]
    else:
        return None

    
    
