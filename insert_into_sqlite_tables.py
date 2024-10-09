
import sqlite3
import json

# connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('imdb_data.db')
cursor = conn.cursor()

# here drop the existing table if it exists (to ensure a fresh start)
cursor.execute('DROP TABLE IF EXISTS upcoming_movies')
cursor.execute('DROP TABLE IF EXISTS fan_favorites')
cursor.execute('DROP TABLE IF EXISTS popular_movies')


# next, I created tables for storing data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS upcoming_movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        release_date TEXT,
        genres TEXT,  -- Add genres column here
        region TEXT
    )
''')

# create the fan_favorites table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS fan_favorites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        release_date TEXT,
        genres TEXT, -- Add genres column here
        rating REAL
    )
''')

# create the popular_movies table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS popular_movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        release_date TEXT,
        genres TEXT, -- add genres column here
        rating REAL
    )
''')

# save changes and commit
conn.commit()

# load data from the JSON file (JSON file generated before in get_data_api.py)
with open("api_data.json", "r") as f:
    api_data = json.load(f)

# Extract the datasets
data_1 = api_data.get("data_1")
data_2 = api_data.get("data_2")
data_3 = api_data.get("data_3")

print("Data 1 (Upcoming Movies):", data_1)
print("Data 2 (Fan Favorites):", data_2)
print("Data 3 (Popular Movies):", data_3)
print(type(data_1))
print(type(data_2))
print(type(data_3))


def insert_upcoming_movies(data):
    if data and "message" in data:
        for group in data["message"]:
            entries = group.get("entries", [])
            for movie in entries:
                title = movie.get("titleText", "")  # access title
                release_date = movie.get("releaseDate", "")  # access release date
                genres = ', '.join(movie.get("genres", []))  # join genres into a single string
                region = 'US'  # take into account US for all entries

                # ensure if title and release_date are not empty before inserting
                if title and release_date:
                    try:
                        cursor.execute('''
                            INSERT INTO upcoming_movies (title, release_date, genres, region)
                            VALUES (?, ?, ?, ?)
                        ''', (title, release_date, genres, region))
                    except Exception as e:
                        print(f"Error during data insertion: {e}")

        # Commit the transaction and fetch all inserted entries to confirm
        conn.commit()
        cursor.execute("SELECT * FROM upcoming_movies;")
        print("Inserted Upcoming Movies:", cursor.fetchall())
    else:
        print("No valid data to insert for upcoming movies.")

# function to insert data into fan favorites table
def insert_fan_favorites(data):
    if data and "message" in data:
        # access list of fan favorites directly
        fan_favorites_list = data["data"].get("list", [])
        if not fan_favorites_list:
            print("No fan favorites to insert.")
            return

        for movie in fan_favorites_list:
            title = movie.get("titleText", {}).get("text", "")
            release_date = movie.get("releaseYear", {}).get("year", "")
            # take into account if genres can be accessed if available in the actual data
            genres = ', '.join(movie.get("genres", []))  # Update as needed if genres are present
            rating = movie.get("ratingsSummary", {}).get("aggregateRating", None)  # Using aggregateRating

            print(f"Inserting Fan Favorite - Title: {title}, Release Date: {release_date}, Genres: {genres}, Rating: {rating}")

            #  ensure title and release_year are not empty before inserting
            if title and release_date:
                try:
                    cursor.execute('''
                        INSERT INTO fan_favorites (title, release_date, genres, rating)
                        VALUES (?, ?, ?, ?)
                    ''', (title, release_date, genres, rating))
                except Exception as e:
                    print(f"Error during fan favorites insertion for {title}: {e}")

        # commit the transaction and fetch all inserted entries to confirm
        conn.commit()
        cursor.execute("SELECT * FROM fan_favorites;")
        print("Inserted Fan Favorites:", cursor.fetchall())
    else:
        print("No valid data to insert for fan favorites.")

def insert_popular_movies(data):
    if not data or not data.get("status", False):
        print("Data is invalid or status is False.")
        return

    # extract a list  of popular movies
    popular_movies_list = data.get("data", {}).get("list", [])
    if not popular_movies_list:
        print("No popular movies to insert.")
        return

    # here I print the entire list to understand its structure
    print("Popular Movies List:", popular_movies_list)

    for movie in popular_movies_list:
        # print the movie to understand its structure
        print("Current Movie Data:", movie)

        title_data = movie.get("title", {})
        title = title_data.get("originalTitleText", {}).get("text", "N/A")
        release_year = title_data.get("releaseYear", {}).get("year", "N/A")
        rating = title_data.get("ratingsSummary", {}).get("aggregateRating", "N/A")

        # extract genres
        genres = title_data.get("titleType", {}).get("categories", [])
        genres_str = ', '.join([genre.get('text', 'N/A') for genre in genres]) if genres else 'N/A'

        print(
            f"Attempting to insert Movie: Title: {title}, Release Year: {release_year}, Genres: {genres_str}, Rating: {rating}")

        # only insert if title and release year are valid
        if title and release_year:
            try:
                cursor.execute('''
                    INSERT INTO popular_movies (title, release_year, genres, rating)
                    VALUES (?, ?, ?, ?)
                ''', (title, release_year, genres_str, rating))
            except Exception as e:
                print(f"Error during popular movies insertion for '{title}': {e}")

    # commit the transaction
    conn.commit()

try:
    # insert data into the tables
    insert_upcoming_movies(data_1)
    insert_fan_favorites(data_2)
    insert_popular_movies(data_3)
    print("Data inserted successfully!")
except Exception as e:
    print("Error during data insertion:", e)

# Example 1: Retrieve all upcoming movies in the US region
cursor.execute("SELECT * FROM upcoming_movies WHERE region = 'US';")
upcoming_us = cursor.fetchall()
print("Upcoming Movies in US:", upcoming_us)


# Example 2: Count movies in each genre
cursor.execute("SELECT genres, COUNT(*) FROM fan_favorites GROUP BY genres;")
genre_count = cursor.fetchall()
print("Count of Movies by Genre:", genre_count)

# Example 3: Retrieve fan favorite movies with a rating greater than 8
cursor.execute("SELECT title, rating FROM popular_movies WHERE rating > 8;")
popular_high_rating = cursor.fetchall()
print("Popular Movies with High Ratings:", popular_high_rating)

# at the end, close the connection
conn.close()

