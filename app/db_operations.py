import mysql.connector

def get_keys(db):
    cursor = db.cursor()
    cursor.execute("SELECT keyword FROM images")
    res = cursor.fetchall()
    cursor.close()
    return res

def add_statistics(db, rows):
    cursor = db.cursor()
    cursor.execute("START TRANSACTION")
    for name, value in rows:
        cursor.execute("INSERT INTO statistics (name, value) VALUES (%s, %s)", (name, value))
    cursor.execute("COMMIT")
    db.commit()
    cursor.close()
    
def clear_statistics(db):
    cursor = db.cursor()
    cursor.execute("START TRANSACTION")
    cursor.execute("TRUNCATE TABLE statistics")
    cursor.execute("COMMIT")
    db.commit()
    cursor.close()

def get_statistics(db):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM statistics")
    res = cursor.fetchall()
    cursor.close()
    return res

def set_key(db, keyword, path):
    cursor = db.cursor()
    cursor.execute("START TRANSACTION")
    cursor.execute("SELECT path FROM images WHERE keyword = %s", (keyword,))
    if cursor.fetchone() is not None:
        cursor.execute("DELETE FROM images WHERE keyword = %s", (keyword,))
    cursor.execute("INSERT INTO images (keyword, path) VALUES (%s, %s)", (keyword, path))
    db.commit()
    cursor.close()

def delete_key(db, keyword):
    cursor = db.cursor()
    cursor.execute("START TRANSACTION")
    cursor.execute("DELETE FROM images WHERE keyword = %s", (keyword,))
    cursor.execute("COMMIT")
    db.commit()
    cursor.close()

def has_key(db, keyword):
    cursor = db.cursor()
    cursor.execute("SELECT path FROM images WHERE keyword = %s", (keyword,))
    res = cursor.fetchone()
    cursor.close()
    return res is not None

def key2filename(db, keyword):
    cursor = db.cursor()
    cursor.execute("SELECT path FROM images WHERE keyword = %s", (keyword,))
    res = cursor.fetchone()
    cursor.close()
    return res

def init_db():
    db = mysql.connector.connect(
        user='root',
        password='longqin0427',
        host='localhost',
        database='group18a1',
    )
    cursor = db.cursor()
    cursor.execute("START TRANSACTION")
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
    cursor.execute("COMMIT")
    db.commit()
    cursor.close()
    return db