import requests
from bs4 import BeautifulSoup

# Define the base URL of the website
base_url = 'https://aviationweather.gov/api/data/metar'
y_n = "yes"

while (y_n == "yes") :
    # Define the search query
    search_query = input("Enter your search query. : ")
    query_to_code = "K" + search_query 
    # Define the search parameters
    search_params = {
        'ids': query_to_code,
        'output': 'html',
        'hours': 1,
        'order': 'ids,obs',
        'q': query_to_code  # Including the search query parameter if necessary
    }
    # Send an HTTP GET request to the API endpoint with the search parameters
    response = requests.get(base_url, params=search_params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
    # Process the search results or perform any desired actions
        print("Search was successful. Processing the search results here.")
        print("Response content:", response.content)
   # data_array = response.get(base_url)
    else:
        print("Failed to perform the search. Status code:", response.status_code)
    # ask if there is another airport input
    y_n = input("would you like to enter a new airport? (yes or no) : ")

# interpret data from searched data
data_found =[
{"id" : "query_to_code","time" : "time","wind" : "wind","visibility" : "visibility","precipitation" : "precipitation","sky" : "sky",
"temperature" : "temperature","altimeter" : "altimeter","remarks" : "remarks"}
] 
parsed_data = []
# for item in data_found :
#      id = item["query_to_code"]
#      time = item["time"]
#      wind = item["wind"]
#      visibility = item["visibility"]
#      precipitation = item["precipitation"]
#      sky = item["sky"]
#      temperature = item["temperature"]
#      altimeter = item["altimeter"]
#      remarks = item["remarks"]
