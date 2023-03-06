from rds import KeyInfo, Statistics, MemcacheStats, AutoConfig
#from utils.ReplacementPolicies import ReplacementPolicies
import mysql.connector
import datetime, time
import decimal

current_time_int = int(time.time())
current_time_tuple = time.localtime(current_time_int)
current_time_str = time.strftime("%Y-%m-%d %H:%M:%S", current_time_tuple)

cnx = mysql.connector.connect(
    user = KeyInfo.db['user'],
    password = KeyInfo.db['password'],
    host = KeyInfo.db['host'],
    database = KeyInfo.db['database'],
)
cursor = cnx.cursor()
create_keyinfo = '''CREATE TABLE IF NOT EXISTS KeyInfo (
                    keyname VARCHAR(255) PRIMARY KEY,
                    path VARCHAR(255) NOT NULL
                )'''
create_statistics = '''CREATE TABLE IF NOT EXISTS Statistics (
                    name VARCHAR(255) PRIMARY KEY,
                    value DECIMAL(65, 3) NOT NULL
                )'''    
create_memcacheStatistics = '''CREATE TABLE IF NOT EXISTS MemcacheStatistics (
                                node INT PRIMARY KEY AUTO_INCREMENT,
                                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                                capacity INT NOT NULL DEFAULT 0,
                                policy INT NOT NULL DEFAULT 0,
                                hitRate DECIMAL(65, 3) NOT NULL DEFAULT 0,
                                missRate DECIMAL(65, 3) NOT NULL DEFAULT 0,
                                numOfItems INT NOT NULL DEFAULT 0,
                                totalSize INT NOT NULL DEFAULT 0,
                                requestPerMinute INT NOT NULL DEFAULT 0
                            )'''  
create_autoconfig = '''CREATE TABLE IF NOT EXISTS AutoConfig (
                                id INT PRIMARY KEY AUTO_INCREMENT,
                                max_MissRate DECIMAL(65, 3) NOT NULL DEFAULT 0,
                                min_MissRate DECIMAL(65, 3) NOT NULL DEFAULT 0,
                                expand_Ratio DECIMAL(65, 3) NOT NULL DEFAULT 0,
                                shrink_Ratio DECIMAL(65, 3) NOT NULL DEFAULT 0
                            )''' 
cursor.execute(create_keyinfo)
cursor.execute(create_statistics)
cursor.execute(create_memcacheStatistics)
cursor.execute(create_autoconfig)
cnx.commit()
cursor.close()
cnx.close()
KeyInfo.delete_all_keys()

#initial settings for statistics
init_stats = [
    ('capacity', 100 * 1024 * 1024),
    ('policy', 0),
    ('requests_count', 0),
    ('hitRate',0.0),
    ('missRAte',0.0),
    ('requests_hit_count', 0),
    ('items_len', 0),
    ('items_bytes', 0),
]

#initial settings for memcache statistics
init_memcacheStats = [
    ('capacity', 100 * 1024 * 1024),
    ('policy', 0),
    ('hitRate',0.0),
    ('missRate',0.0),
    ('numOfItems',0),
    ('totalSize', 0),
    ('requestPerMinute', 0),
]

#initial settings for autoconfig
init_autoconfig = [
    ('max_MissRate', 0.0),
    ('min_MissRate', 0.0),
    ('expand_Ratio', 0.0),
    ('shrink_Ratio', 0.0),
]


Statistics.add_statistics(init_stats)
MemcacheStats.add_MemcacheStatistics(init_memcacheStats)
AutoConfig.init_AutoConfig(init_autoconfig)


#test for mem stats ---->  MemcacheStats.update_MemcacheStatistics('totalSize', 10233188, 1)
#test --->  print(MemcacheStats.get_MemcacheStaticstics(1, 'policy'))

#test for auto config ---->  AutoConfig.update_AutoConfig('max_MissRate', 50.0)

