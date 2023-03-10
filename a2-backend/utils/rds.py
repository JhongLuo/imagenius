import mysql.connector
from utils.ReplacementPolicies import ReplacementPolicies
from enum import Enum

class StatsNames(Enum):
    # total_requests = "total_requests"
    # read_requests = "read_requests"
    # missed_requests = "missed_requests"
    replacement_policy = "replacement_policy"
    max_size = "max_size"
        
database_name = "ece1779a2"

config = {
    "pool_name" : "group18a2_pool",
    "pool_size" : 1,
    "user" : "root",
    "password" : "ece1779pass",
    "host" : "ece1779a2.cvtl8zx5dggi.us-east-1.rds.amazonaws.com",
    "database" : database_name,
}

def cursor_operation(func):
    def wrapper(*args, **kwargs):
        conn = mysql.connector.connect(**config)
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
    new_config = config.copy()
    new_config.pop("database")
    new_config.pop("pool_size")
    new_config.pop("pool_name")
    conn = mysql.connector.connect(**new_config)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
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
def reset_memcache_status(cursor):
    for i in range(8):
        cursor.execute(f"INSERT INTO memcache (id, is_started) VALUES ({i}, FALSE) ON DUPLICATE KEY UPDATE is_started = FALSE")

@cursor_operation
def get_memcache_status(cursor, id):
    if id >= 0 and id < 8:
        cursor.execute(f"SELECT is_started FROM memcache WHERE id = {id}")
        return bool(cursor.fetchone()[0])
    else:
        raise Exception("Invalid memcache id")

@cursor_operation
def set_memcache_status(cursor, id, status):
    if id >= 0 and id < 8:
        cursor.execute(f"UPDATE memcache SET is_started = {status} WHERE id = {id}")
    else:
        raise Exception("Invalid memcache id")

@cursor_operation
def reset_auto_scaler_status(cursor):
    cursor.execute(f"INSERT INTO memcache (id, is_started) VALUES (8, FALSE) ON DUPLICATE KEY UPDATE is_started = FALSE")

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
        # (StatsNames.total_requests.value, 0),
        # (StatsNames.read_requests.value, 0),
        # (StatsNames.missed_requests.value, 0),
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
    cursor.execute(f"SELECT value FROM stats WHERE name = '{name.value}'")
    res = cursor.fetchone()
    return int(res[0])

# @cursor_operation
# def add_stat(cursor, name : StatsNames, value):
#     if name == StatsNames.total_requests or name == StatsNames.read_requests or name == StatsNames.missed_requests:
#         cursor.execute(f"UPDATE stats SET value = value + {str(value)} WHERE name = '{name.value}'")
#     else:
#         raise Exception("Cannot add to this stat")

# @cursor_operation
# def set_stat(cursor, name : StatsNames, value):
#     if name == StatsNames.max_size or name == StatsNames.replacement_policy:
#         cursor.execute(f"UPDATE stats SET value = {str(value)} WHERE name = '{name.value}'")
#     else:
#         raise Exception("Cannot set this stat")
    
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
def key2path(cursor, keyword):
    cursor.execute("SELECT path FROM images WHERE keyword = %s", (keyword,))
    res = cursor.fetchone()
    if res:
        return res[0]
    else:
        return None

    
    
