import mysql.connector

class DBConnector:
    def __init__(self):
        pass
    
    @staticmethod
    def delete_keys():
        sql_connector = mysql.connector.connect(
            pool_name = "group18a1_pool",
            pool_size = 16,
            user='root',
            password='ece1779pass',
            host='localhost',
            database='group18a1',
        )
        cursor = sql_connector.cursor()
        cursor.execute("TRUNCATE TABLE images")
        sql_connector.commit()
        cursor.close()
        sql_connector.close()

    @staticmethod
    def get_keys():
        sql_connector = mysql.connector.connect(
            pool_name = "group18a1_pool",
            pool_size = 16,
            user='root',
            password='ece1779pass',
            host='localhost',
            database='group18a1',
        )
        cursor = sql_connector.cursor()
        cursor.execute("SELECT keyword FROM images")
        res = cursor.fetchall()
        cursor.close()
        sql_connector.close()
        return [x[0] for x in res]

    @staticmethod
    def set_statistics(rows):
        sql_connector = mysql.connector.connect(
            pool_name = "group18a1_pool",
            pool_size = 16,
            user='root',
            password='ece1779pass',
            host='localhost',
            database='group18a1',
        )
        cursor = sql_connector.cursor()
        for name, value in rows:
            cursor.execute("UPDATE statistics SET value = %s WHERE name = %s", (value, name))
        sql_connector.commit()
        cursor.close()
        sql_connector.close()
    
    @staticmethod
    def add_statistics(rows):
        sql_connector = mysql.connector.connect(
            pool_name = "group18a1_pool",
            pool_size = 16,
            user='root',
            password='ece1779pass',
            host='localhost',
            database='group18a1',
        )
        cursor = sql_connector.cursor()
        cursor.execute("TRUNCATE TABLE statistics")
        for name, value in rows:
            cursor.execute("INSERT INTO statistics (name, value) VALUES (%s, %s)", (name, value))
        sql_connector.commit()
        cursor.close()
        sql_connector.close()
    
    @staticmethod
    def select_statistics(key):
        sql_connector = mysql.connector.connect(
            pool_name = "group18a1_pool",
            pool_size = 16,
            user='root',
            password='ece1779pass',
            host='localhost',
            database='group18a1',
        )
        cursor = sql_connector.cursor()
        cursor.execute("SELECT value FROM statistics WHERE name = %s", (key,))
        res = cursor.fetchone()
        cursor.close()
        sql_connector.close()
        if res:
            return res[0]
        else:
            return None
    
    @staticmethod
    def set_key(keyword, path):
        sql_connector = mysql.connector.connect(
            pool_name = "group18a1_pool",
            pool_size = 16,
            user='root',
            password='ece1779pass',
            host='localhost',
            database='group18a1',
        )
        cursor = sql_connector.cursor()
        cursor.execute("SELECT path FROM images WHERE keyword = %s", (keyword,))
        if cursor.fetchone() is not None:
            cursor.execute("UPDATE images SET path = %s WHERE keyword = %s", (path, keyword))
        else:
            cursor.execute("INSERT INTO images (keyword, path) VALUES (%s, %s)", (keyword, path))
        sql_connector.commit()
        cursor.close()
        sql_connector.close()

    @staticmethod
    def delete_key(keyword):
        sql_connector = mysql.connector.connect(
            pool_name = "group18a1_pool",
            pool_size = 16,
            user='root',
            password='ece1779pass',
            host='localhost',
            database='group18a1',
        )
        cursor = sql_connector.cursor()
        cursor.execute("DELETE FROM images WHERE keyword = %s", (keyword,))
        sql_connector.commit()
        cursor.close()
        sql_connector.close()

    @staticmethod
    def key2path(keyword):
        sql_connector = mysql.connector.connect(
            pool_name = "group18a1_pool",
            pool_size = 16,
            user='root',
            password='ece1779pass',
            host='localhost',
            database='group18a1',
        )
        cursor = sql_connector.cursor()
        cursor.execute("SELECT path FROM images WHERE keyword = %s", (keyword,))
        res = cursor.fetchone()
        cursor.close()
        sql_connector.close()
        if res:
            return res[0]
        else:
            return None
