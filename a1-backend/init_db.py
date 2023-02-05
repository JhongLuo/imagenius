from utils.DBConnector import DBConnector
from utils.ReplacementPolicies import ReplacementPolicies
import mysql.connector

cnx = mysql.connector.connect(
            user='root',
            password='ece1779pass',
            host='localhost',
            database='group18a1',
)
cursor = cnx.cursor()
create_images = '''CREATE TABLE IF NOT EXISTS images (
                    keyword VARCHAR(255) PRIMARY KEY,
                    path VARCHAR(255) NOT NULL
                )'''
create_statistics = '''CREATE TABLE IF NOT EXISTS statistics (
                    name VARCHAR(255) PRIMARY KEY,
                    value DECIMAL(65, 3) NOT NULL
                )'''    

cursor.execute(create_images)
cursor.execute(create_statistics)
cnx.commit()
cursor.close()
cnx.close()
DBConnector.delete_keys()

initial_data = [
    ('max_size', 100 * 1024 * 1024),
    ('replacement_policy', ReplacementPolicies.LRU.value),
    ('requests_count', 0),
    ('requests_hit_count', 0),
    ('items_len', 0),
    ('items_bytes', 0),
]

DBConnector.add_statistics(initial_data)
