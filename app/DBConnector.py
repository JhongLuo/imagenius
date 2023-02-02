import mysql.connector
import threading


class DBConnector:
    def __init__(self):
        self.sql_connector = mysql.connector.connect(
            user='root',
            password='ece1779pass',
            host='localhost',
            database='group18a1',
        )
        cursor = self.sql_connector.cursor()
        cursor.execute("START TRANSACTION")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        for table in tables:
            cursor.execute("DROP TABLE {}".format(table[0]))

        create_images = '''CREATE TABLE images (
                                    keyword VARCHAR(255) PRIMARY KEY,
                                    path VARCHAR(255) NOT NULL
                            )'''
        create_statistics = '''CREATE TABLE statistics (
                                    name VARCHAR(255) PRIMARY KEY,
                                    value DECIMAL(65, 3) NOT NULL
                            )'''    
        cursor.execute(create_images)
        cursor.execute(create_statistics)
        cursor.execute("COMMIT")
        self.sql_connector.commit()
        cursor.close()
        self.statistic_lock = threading.Lock()
        self.images_lock = threading.Lock()

    def get_keys(self):
        cursor = self.sql_connector.cursor()
        cursor.execute("SELECT keyword FROM images")
        res = cursor.fetchall()
        cursor.close()
        return res

    def set_statistics(self, rows):
        with self.statistic_lock:
            cursor = self.sql_connector.cursor()
            cursor.execute("START TRANSACTION")
            for name, value in rows:
                cursor.execute("UPDATE statistics SET value = %s WHERE name = %s", (value, name))
            cursor.execute("COMMIT")
            self.sql_connector.commit()
            cursor.close()
            
    def add_statistics(self, rows):
        with self.statistic_lock:
            cursor = self.sql_connector.cursor()
            cursor.execute("START TRANSACTION")
            cursor.execute("TRUNCATE TABLE statistics")
            for name, value in rows:
                cursor.execute("INSERT INTO statistics (name, value) VALUES (%s, %s)", (name, value))
            cursor.execute("COMMIT")
            self.sql_connector.commit()
            cursor.close()

    def get_statistics(self):
        cursor = self.sql_connector.cursor()
        cursor.execute("SELECT * FROM statistics")
        res = cursor.fetchall()
        cursor.close()
        return res

    def set_key(self, keyword, path):
        with self.images_lock:
            cursor = self.sql_connector.cursor()
            cursor.execute("START TRANSACTION")
            cursor.execute("SELECT path FROM images WHERE keyword = %s", (keyword,))
            if cursor.fetchone() is not None:
                cursor.execute("DELETE FROM images WHERE keyword = %s", (keyword,))
            cursor.execute("INSERT INTO images (keyword, path) VALUES (%s, %s)", (keyword, path))
            self.sql_connector.commit()
            cursor.close()

    def delete_key(self, keyword):
        with self.images_lock:
            cursor = self.sql_connector.cursor()
            cursor.execute("START TRANSACTION")
            cursor.execute("DELETE FROM images WHERE keyword = %s", (keyword,))
            cursor.execute("COMMIT")
            self.sql_connector.commit()
            cursor.close()

    def key2path(self, keyword):
        cursor = self.sql_connector.cursor()
        cursor.execute("SELECT path FROM images WHERE keyword = %s", (keyword,))
        res = cursor.fetchone()
        cursor.close()
        if res:
            return res[0]
        else:
            return None
