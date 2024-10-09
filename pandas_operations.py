import sqlite3
import pandas as pd

# connect to SQLite database
conn = sqlite3.connect('imdb_data.db')

#  load data into Pandas DataFrames
upcoming_movies_df = pd.read_sql_query("SELECT * FROM upcoming_movies", conn)
fan_favorites_df = pd.read_sql_query("SELECT * FROM fan_favorites", conn)
popular_movies_df = pd.read_sql_query("SELECT * FROM popular_movies", conn)

# Convert the release_date columns to datetime format
upcoming_movies_df['release_date'] = pd.to_datetime(upcoming_movies_df['release_date'], errors='coerce')
fan_favorites_df['release_date'] = pd.to_datetime(fan_favorites_df['release_date'], errors='coerce')

# Calculate KPIs using .agg()
# KPI 1: Average Rating of Fan Favorites using .agg()
average_rating = fan_favorites_df.agg({'rating': 'mean'}).iloc[0]
print(f"Average Rating of Fan Favorites: {average_rating:.2f}")


# KPI 2: Total Number of Movies Released Per Year using .agg()
movies_per_year = upcoming_movies_df.groupby(upcoming_movies_df['release_date'].dt.year).agg({'id': 'count'}).rename(columns={'id': 'total_movies'})
print("\nTotal Number of Movies Released Per Year:")
print(movies_per_year)

# Next is an example for calculating multiple KPIs at once
summary_stats = fan_favorites_df.agg({'rating': ['mean', 'min', 'max']})
print("Summary Statistics for Fan Favorites Ratings:")
print(summary_stats)

# close the database connection
conn.close()