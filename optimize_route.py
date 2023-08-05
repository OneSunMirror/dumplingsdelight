import requests
import googlemaps
from googlemaps import distance_matrix
url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="
map_api_key = "AIzaSyDILOATa9jdhX1tQqsYiS-ALgKSzZ6pesM"
gmaps = googlemaps.Client(key=map_api_key)
def find_route(locations):
    gmaps = googlemaps.Client(key=map_api_key)
    return gmaps.distance_matrix(locations, locations)