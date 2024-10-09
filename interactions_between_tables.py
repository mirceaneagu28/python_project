import sqlite3

# connect to SQLite database
conn = sqlite3.connect('imdb_data.db')
cursor = conn.cursor()

# enable foreign key constraint support
cursor.execute("PRAGMA foreign_keys = ON;")

# drop existing tables if they exist
cursor.execute('DROP TABLE IF EXISTS movies')
cursor.execute('DROP TABLE IF EXISTS upcoming_movies')
cursor.execute('DROP TABLE IF EXISTS fan_favorites')
cursor.execute('DROP TABLE IF EXISTS popular_movies')

#  Create a central movies table with a unique movie_id
cursor.execute('''
    CREATE TABLE movies (
        movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT UNIQUE NOT NULL,
        release_date TEXT,
        genres TEXT
    )
''')

# modify upcoming_movies table to reference the movies table
cursor.execute('''
    CREATE TABLE upcoming_movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        movie_id INTEGER,
        region TEXT,
        FOREIGN KEY (movie_id) REFERENCES movies (movie_id)
    )
''')

# modify fan_favorites table to reference the movies table
cursor.execute('''
    CREATE TABLE fan_favorites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        movie_id INTEGER,
        rating REAL,
        FOREIGN KEY (movie_id) REFERENCES movies (movie_id)
    )
''')

# modify popular_movies table to reference the movies table
cursor.execute('''
    CREATE TABLE popular_movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        movie_id INTEGER,
        rating REAL,
        FOREIGN KEY (movie_id) REFERENCES movies (movie_id)
    )
''')

# commit the changes
conn.commit()

# Show the tables here to confirm the structure
print("Tables created with relationships:")
for row in cursor.execute("SELECT name FROM sqlite_master WHERE type='table';"):
    print(row[0])

# then, close the connection
conn.close()