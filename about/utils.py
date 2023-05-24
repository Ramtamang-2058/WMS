import requests
import urllib.parse


def get_route_matrix(api_key, locations):
    url = "https://graphhopper.com/api/1/matrix"
    points = ["48.8567,2.3508", "51.5072,-0.1276", "40.7128,-74.0060"]

    # Define the locations you want to route between
    locations = [
    "2.3508,48.8567",  # Paris, France
    "-0.1276,51.5072",  # London, UK
    "-74.0060,40.7128"  # New York City, USA
]

# Build the request query
    query = {
    "profile": "car",
    "point": "|".join(points),
    "out_array": "distances",
    "fail_fast": "true",
    "key": api_key
}

# Send the request to the API and parse the response
    response = requests.get(url, params=query)
    matrix = response.json()

# Print the distance matrix
    print(matrix)
    # distances = matrix['distances']
    # times = matrix['times']
    return 0