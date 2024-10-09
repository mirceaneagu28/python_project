import sqlite3

# connect to SQLite database
conn = sqlite3.connect('imdb_data.db')
cursor = conn.cursor()

# SQL query to count upcoming movies by release region
cursor.execute('''
    SELECT region, COUNT(*) as movie_count
    FROM upcoming_movies
    GROUP BY region
    ORDER BY movie_count DESC
''')

upcoming_movies_by_region = cursor.fetchall()

# display the report
if upcoming_movies_by_region:
    print("Report: Count of Upcoming Movies by Region")
    for region, count in upcoming_movies_by_region:
        print(f"Region: {region}, Total Upcoming Movies: {count}")
else:
    print("No upcoming movies found.")

# close the connection
conn.close()

#This report counts the number of upcoming movies in each region.
#Output: It displays the regions and the total count of movies scheduled for release in each

