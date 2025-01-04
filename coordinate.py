import time
from geopy.geocoders import Nominatim

def get_coordinates(city_name):
    geolocator = Nominatim(user_agent="weather-app")
    location = geolocator.geocode(city_name)
    if location:
        return (location.latitude, location.longitude)
    else:
        return None

# # Example usage with a delay to prevent rate-limiting
# city = "Seri Kembangan"
# coordinates = get_coordinates(city)
# time.sleep(1)  # Adding a delay of 1 second between requests to avoid hitting rate limits

# if coordinates:
#     print(f"The coordinates of {city} are: Latitude = {coordinates[0]}, Longitude = {coordinates[1]}")
# else:
#     print(f"Could not get coordinates for {city}")
