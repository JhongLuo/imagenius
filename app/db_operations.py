import mysql.connector

def add_statistics(db, name, value):
    cursor = db.cursor()
    cursor.execute("INSERT INTO statistics (name, value) VALUES (%s, %s)", (name, value))
    db.commit()
    cursor.close()
    
def clear_statistics(db):
    cursor = db.cursor()
    cursor.execute("DELETE FROM statistics")
    db.commit()
    cursor.close()

def update_statistics(db, name, value):
    cursor = db.cursor()
    cursor.execute("UPDATE statistics SET value = %s WHERE name = %s", (value, name))
    db.commit()
    cursor.close()
    
def get_statistics(db, name):
    cursor = db.cursor()
    cursor.execute("SELECT value FROM statistics WHERE name = %s", (name,))
    db.commit()
    cursor.close()

def add_image(db, keyword, path):
    cursor = db.cursor()
    cursor.execute("INSERT INTO images (keyword, path) VALUES (%s, %s)", (keyword, path))
    db.commit()
    cursor.close()

def delete_image(db, keyword):
    cursor = db.cursor()
    cursor.execute("DELETE FROM images WHERE keyword = %s", (keyword,))
    db.commit()
    cursor.close()

def init_db():
    db = mysql.connector.connect(
        user='root',
        host='localhost',
        database='group18a1',
    )
    cursor = db.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    for table in tables:
        cursor.execute("DROP TABLE {}".format(table[0]))
        print("Table {} deleted".format(table[0]))

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
    db.commit()
    cursor.close()
    return db