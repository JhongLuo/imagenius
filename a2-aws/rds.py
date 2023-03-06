import mysql.connector
import datetime
import time

class KeyInfo:
    
    db = {'user': 'root',
          'password': 'longqin0427',
          'host': 'localhost',
          'database': 'A2'}
    
    def __init(self):
        pass
    
    @staticmethod
    def delete_all_keys():
        sql_connector = mysql.connector.connect(
            user = KeyInfo.db['user'],
            password = KeyInfo.db['password'],
            host = KeyInfo.db['host'],
            database = KeyInfo.db['database'],
        )
        
        cursor = sql_connector.cursor()
        query = "TRUNCATE TABLE KeyInfo"
        cursor.execute(query)
        sql_connector.commit()
        cursor.close()
        sql_connector.close()
    
    @staticmethod
    def get_all_keys():
        sql_connector = mysql.connector.connect(
            user = KeyInfo.db['user'],
            password = KeyInfo.db['password'],
            host = KeyInfo.db['host'],
            database = KeyInfo.db['database'],
        )
        cursor = sql_connector.cursor()
        query = "SELECT keyname FROM KeyInfo"
        cursor.execute(query)
        res = cursor.fetchall()
        cursor.close()
        sql_connector.close()
        return [x[0] for x in res]
    
    @staticmethod
    def set_key(keyname, path):
        sql_connector = mysql.connector.connect(
            user = KeyInfo.db['user'],
            password = KeyInfo.db['password'],
            host = KeyInfo.db['host'],
            database = KeyInfo.db['database'],
        )
        cursor = sql_connector.cursor()
        query1 = "SELECT path FROM KeyInfo WHERE keyname = %s"
        cursor.execute(query1, (keyname,))
        if cursor.fetchone() is not None:
            query2 = "UPDATE KeyInfo SET path = %s WHERE keyname = %s"
            cursor.execute(query2, (path, keyname))
        else:
            query3 = "INSERT INTO KeyInfo (keyname, path) VALUES (%s, %s)"
            cursor.execute(query3, (keyname, path))
        sql_connector.commit()
        cursor.close()
        sql_connector.close()
        
    @staticmethod
    def delete_key(keyname):
        sql_connector = mysql.connector.connect(
            user = KeyInfo.db['user'],
            password = KeyInfo.db['password'],
            host = KeyInfo.db['host'],
            database = KeyInfo.db['database'],
        )
        cursor = sql_connector.cursor()
        query = "DELETE FROM KeyInfo WHERE keyname = %s"
        cursor.execute(query, (keyname,))
        sql_connector.commit()
        cursor.close()
        sql_connector.close()
        
    @staticmethod
    def key2path(keyname):
        sql_connector = mysql.connector.connect(
            user = KeyInfo.db['user'],
            password = KeyInfo.db['password'],
            host = KeyInfo.db['host'],
            database = KeyInfo.db['database'],
        )
        cursor = sql_connector.cursor()
        query = "SELECT path FROM KeyInfo WHERE keyname = %s"
        cursor.execute(query, (keyname,))
        res = cursor.fetchone()
        cursor.close()
        sql_connector.close()
        if res:
            return res[0]
        else:
            return None


class Statistics:
    def __init__(self):
        pass

    @staticmethod
    def update_statistics(rows):
        sql_connector = mysql.connector.connect(
            user = KeyInfo.db['user'],
            password = KeyInfo.db['password'],
            host = KeyInfo.db['host'],
            database = KeyInfo.db['database'],
        )
        cursor = sql_connector.cursor()
        for name, value in rows:
            query = "UPDATE Statistics SET value = %s WHERE name = %s"
            cursor.execute(query, (value, name))
        sql_connector.commit()
        cursor.close()
        sql_connector.close()
        
    @staticmethod
    def add_statistics(rows):
        sql_connector = mysql.connector.connect(
            user = KeyInfo.db['user'],
            password = KeyInfo.db['password'],
            host = KeyInfo.db['host'],
            database = KeyInfo.db['database'],
        )
        cursor = sql_connector.cursor()
        query1 = "TRUNCATE TABLE Statistics"
        cursor.execute(query1)
        for name, value in rows:
            query2 = "INSERT INTO Statistics (name, value) VALUES (%s, %s)"
            cursor.execute(query2, (name, value))
        sql_connector.commit()
        cursor.close()
        sql_connector.close()
    
    @staticmethod
    def get_staticstics(key):
        sql_connector = mysql.connector.connect(
            user = KeyInfo.db['user'],
            password = KeyInfo.db['password'],
            host = KeyInfo.db['host'],
            database = KeyInfo.db['database'],
        )
        cursor = sql_connector.cursor()
        query = "SELECT value FROM Statistics WHERE name = %s"
        cursor.execute(query, (key,))
        res = cursor.fetchone()
        cursor.close()
        sql_connector.close()
        if res:
            return res[0]
        else:
            return None
    
class MemcacheStats:
    
    def __init__(self):
        pass
    
    @staticmethod
    def add_MemcacheStatistics(rows):
        sql_connector = mysql.connector.connect(
            user = KeyInfo.db['user'],
            password = KeyInfo.db['password'],
            host = KeyInfo.db['host'],
            database = KeyInfo.db['database'],
        )
        cursor = sql_connector.cursor()
        #query1 = "TRUNCATE TABLE MemcacheStatistics"
        #cursor.execute(query1)
        columns = ', '.join([row[0] for row in rows])
        values = ', '.join(['%s' for row in rows])
        query2 = f"INSERT INTO MemcacheStatistics ({columns}) VALUES ({values})"
        cursor.execute(query2, [row[1] for row in rows])
        sql_connector.commit()
        cursor.close()
        sql_connector.close()
        
    @staticmethod
    def get_MemcacheStaticstics(column, node):
        sql_connector = mysql.connector.connect(
            user=KeyInfo.db['user'],
            password=KeyInfo.db['password'],
            host=KeyInfo.db['host'],
            database=KeyInfo.db['database'],
        )
        cursor = sql_connector.cursor()
        query = f"SELECT {column} FROM MemcacheStatistics WHERE node = %s"
        cursor.execute(query, (node,))
        res = cursor.fetchone()
        cursor.close()
        sql_connector.close()
        if res:
            return res[0]
        else:
            return None

    
    
    @staticmethod
    def update_MemcacheStatistics(column, value, node):
        sql_connector = mysql.connector.connect(
            user = KeyInfo.db['user'],
            password = KeyInfo.db['password'],
            host = KeyInfo.db['host'],
            database = KeyInfo.db['database'],
        )
        cursor = sql_connector.cursor()

        query = "UPDATE MemcacheStatistics SET {} = %s WHERE node = %s".format(column)
        cursor.execute(query, (value, node))
        sql_connector.commit()
        cursor.close()
        sql_connector.close()

       
    @staticmethod    
    def get_Formatted_MemcacheStaticstics(node):
        sql_connector = mysql.connector.connect(
            user = KeyInfo.db['user'],
            password = KeyInfo.db['password'],
            host = KeyInfo.db['host'],
            database = KeyInfo.db['database'],
        )
        cursor = sql_connector.cursor()
        #query = "SELECT totalSize FROM MemcacheStatistics WHERE node = 0"
        query = "SELECT DATE_FORMAT(timestamp, '%Y-%m-%d %H:%i'), TRUNCATE(AVG(missRate), 3), TRUNCATE(AVG(hitRate), 3), SUM(numOfItems), TRUNCATE(totalSize/(1024*1024), 1),  SUM(requestPerMinute) FROM MemcacheStatistics where node = %s"
        cursor.execute(query, (node,))
        res = cursor.fetchall()
        cursor.close()
        sql_connector.close()
        if res:
            return [x[i] for x in res for i in range(len(x))]
        else:
            return None
        

class AutoConfig:
    def __init__(self):
        pass
    
    @staticmethod
    def init_AutoConfig(rows):
        sql_connector = mysql.connector.connect(
            user = KeyInfo.db['user'],
            password = KeyInfo.db['password'],
            host = KeyInfo.db['host'],
            database = KeyInfo.db['database'],
        )
        cursor = sql_connector.cursor()
        query1 = "TRUNCATE TABLE AutoConfig"
        cursor.execute(query1)
        columns = ', '.join([row[0] for row in rows])
        values = ', '.join(['%s' for row in rows])
        query2 = f"INSERT INTO AutoConfig ({columns}) VALUES ({values})"
        cursor.execute(query2, [row[1] for row in rows])
        sql_connector.commit()
        cursor.close()
        sql_connector.close()
        
    @staticmethod
    def get_AutoConfig(column):
        sql_connector = mysql.connector.connect(
            user=KeyInfo.db['user'],
            password=KeyInfo.db['password'],
            host=KeyInfo.db['host'],
            database=KeyInfo.db['database'],
        )
        cursor = sql_connector.cursor()
        query = f"SELECT {column} FROM AutoConfig WHERE id = 1"
        cursor.execute(query)
        res = cursor.fetchone()
        cursor.close()
        sql_connector.close()
        if res:
            return res[0]
        else:
            return None

    
    
    @staticmethod
    def update_AutoConfig(column, value):
        sql_connector = mysql.connector.connect(
            user = KeyInfo.db['user'],
            password = KeyInfo.db['password'],
            host = KeyInfo.db['host'],
            database = KeyInfo.db['database'],
        )
        cursor = sql_connector.cursor()

        query = "UPDATE AutoConfig SET {} = %s WHERE id = 1".format(column)
        cursor.execute(query, (value,))
        sql_connector.commit()
        cursor.close()
        sql_connector.close()

       
    @staticmethod    
    def get_Formatted_AutoConfig():
        sql_connector = mysql.connector.connect(
            user = KeyInfo.db['user'],
            password = KeyInfo.db['password'],
            host = KeyInfo.db['host'],
            database = KeyInfo.db['database'],
        )
        cursor = sql_connector.cursor()
        query = "SELECT TRUNCATE(AVG(max_MissRate), 3), TRUNCATE(AVG(min_MissRate), 3),TRUNCATE(AVG(expand_Ratio), 3),TRUNCATE(AVG(shrink_Ratio), 3) FROM AutoConfig where id = 1"
        cursor.execute(query)
        res = cursor.fetchall()
        cursor.close()
        sql_connector.close()
        if res:
            return [x[i] for x in res for i in range(len(x))]
        else:
            return None
    