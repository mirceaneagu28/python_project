import requests
import json

# the RapidAPI key
api_key = "ac08e9451dmsh3644c231933df41p136d57jsnbf4d7a531e8a"  # Replace with your actual API key

data_1 = None
data_2 = None
data_3 = None

# IMDB API endpoint URL1
url_1 = "https://imdb188.p.rapidapi.com/api/v1/getUpcomingMovies"

#url = "https://rapidapi.com/DataCrawler/api/imdb188/playground/apiendpoint_b62dbecb-bad7-41ca-ac82-56be8f1841f6"
#url = "https://imdb188.p.rapidapi.com/api/v1/getPop"

# headers for authentication
headers_1 = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": "imdb188.p.rapidapi.com"
}

# example of query parameters (we can change it based on requirements)
querystring_1 = {"region":"US"}  # Example actor ID (e.g., Johnny Depp)

# I send here a GET request to the API endpoint
response_1 = requests.get(url_1, headers=headers_1, params=querystring_1)

# here it's a check to see if the request was successful
if response_1.status_code == 200:
    # here parse the JSON response
    data_1 = response_1.json()
    print("API Data 1:", data_1)
else:
    print(f"Error: Unable to retrieve data (Status code: {response_1.status_code})")





url_2 = "https://imdb188.p.rapidapi.com/api/v1/getFanFavorites"

headers_2 = {
	"x-rapidapi-key": api_key,
	"x-rapidapi-host": "imdb188.p.rapidapi.com"
}

querystring_2 = {"country":"US"}

response_2 = requests.get(url_2, headers=headers_2, params=querystring_2)

#Check if the request was successful
if response_2.status_code == 200:
    # Parse the JSON response
    data_2 = response_2.json()
    print("API Data 2:", data_2)
else:
    print(f"Error: Unable to retrieve data (Status code: {response_2.status_code})")


url_3 = "https://imdb188.p.rapidapi.com/api/v1/getPopularMovies"

payload_3 = {
	"country": { "anyPrimaryCountries": ["IN"] },
	"limit": 200,
	"releaseDate": { "releaseDateRange": {
			"end": "2029-12-31",
			"start": "2020-01-01"
		} },
	"userRatings": {
		"aggregateRatingRange": {
			"max": 10,
			"min": 6
		},
		"ratingsCountRange": { "min": 1000 }
	},
	"genre": { "allGenreIds": ["Action"] },
	"runtime": { "runtimeRangeMinutes": {
			"max": 120,
			"min": 0
		} }
}
headers_3 = {
	"x-rapidapi-key": api_key,
	"x-rapidapi-host": "imdb188.p.rapidapi.com",
	"Content-Type": "application/json"
}

response_3 = requests.post(url_3, json=payload_3, headers=headers_3)

#Check if the request was successful
if response_3.status_code == 200:
    # Parse the JSON response
    data_3 = response_3.json()
    print("API Data 3:", data_3)
else:
    print(f"Error: Unable to retrieve data (Status code: {response_3.status_code})")

if data_1 and data_2 and data_3:
    # Save data to a JSON file
    with open("api_data.json", "w") as f:
        json.dump({"data_1": data_1, "data_2": data_2, "data_3": data_3}, f)
    print("Data fetched and saved to api_data.json!")
else:
    print("Error: One or more datasets are missing. JSON file not saved.")