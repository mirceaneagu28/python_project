import sqlite3

#  connect to the SQLite database
conn = sqlite3.connect('imdb_data.db')
cursor = conn.cursor()

# Then: Execute SQL queries and fetch results

# Example 1: Retrieve all upcoming movies in the US region
cursor.execute("SELECT * FROM upcoming_movies WHERE region = 'US';")
upcoming_us = cursor.fetchall()
print("Upcoming Movies in US:")
for movie in upcoming_us:
    print(movie)

# Example 2: Count movies in each genre
cursor.execute("SELECT genres, COUNT(*) FROM fan_favorites GROUP BY genres;")
genre_count = cursor.fetchall()
print("\nCount of Movies by Genre:")
for genre in genre_count:
    print(f"Genre: {genre[0]}, Count: {genre[1]}")

# Example 3: Retrieve fan favorite movies with a rating greater than 8
cursor.execute("SELECT title, rating FROM fan_favorites WHERE rating > 8;")
popular_high_rating = cursor.fetchall()
print("\nFan Favorite Movies with High Ratings (Rating > 8):")
for movie in popular_high_rating:
    print(f"Title: {movie[0]}, Rating: {movie[1]}")

# close the connection
conn.close()