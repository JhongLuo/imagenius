from utils.DBConnector import DBConnector
from utils.ReplacementPolicies import ReplacementPolicies
db = DBConnector()

cnx = db.sql_connector
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

db.delete_keys()
initial_data = [
    ('max_size', 10000000),
    ('replacement_policy', ReplacementPolicies.LRU.value),
    ('requests_count', 0),
    ('requests_hit_count', 0),
    ('items_len', 0),
    ('items_bytes', 0),
]
db.add_statistics(initial_data)
db.close()