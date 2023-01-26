import mysql.connector

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
    cursor.close()
    db.commit()
    
    return db