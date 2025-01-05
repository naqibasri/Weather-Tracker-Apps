import azure.functions as func
import datetime
import json
import logging
import requests
import os
from dotenv import load_dotenv
import coordinate 
load_dotenv()

app = func.FunctionApp()

API_KEY = os.getenv("openweather_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


@app.route(route="SendWeatherAlert", auth_level=func.AuthLevel.ANONYMOUS)
def SendWeatherAlert(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Weather Alert Function triggered.")

    try:
        # Get the city parameter from the request
        city = req.params.get("city")
        if not city:
            return func.HttpResponse("Please provide a city name.", status_code=400)

        # Get the threshold temperature, default to 20°C
        threshold_temp = float(req.params.get("threshold_temp", 20))

        # Get coordinates for the city
        coordinates = coordinate.get_coordinates(city)
        if not coordinates:
            return func.HttpResponse(f"Could not find coordinates for {city}.", status_code=400)

        # Fetch weather data for the city using coordinates
        response = requests.get(BASE_URL, params={
            "lat": coordinates[0],
            "lon": coordinates[1],
            "units": "metric",  # Use Celsius
            "appid": API_KEY
        })

        # Handle unsuccessful API response
        response.raise_for_status()
        weather_data = response.json()

        # Check if the weather data contains the expected structure
        if "main" not in weather_data or "temp" not in weather_data["main"]:
            return func.HttpResponse("Error: Could not retrieve weather data.", status_code=500)

        # Get the current temperature from the weather data
        current_temp = weather_data["main"]["temp"]

        # Check if the temperature exceeds the threshold
        if current_temp > threshold_temp:
            alert_message = f"Alert! The temperature in {city} is {current_temp}°C, which exceeds the threshold of {threshold_temp}°C."
        else:
            alert_message = f"The temperature in {city} is {current_temp}°C. No alert."

        return func.HttpResponse(alert_message, status_code=200)

    except requests.exceptions.RequestException as req_err:
        logging.error(f"Request error occurred: {req_err}")
        return func.HttpResponse("An error occurred while fetching weather data.", status_code=500)
    except ValueError as val_err:
        logging.error(f"Value error: {val_err}")
        return func.HttpResponse("Invalid data provided.", status_code=400)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return func.HttpResponse("An unexpected error occurred.", status_code=500)
    # logging.info('Python HTTP trigger function processed a request.')

    # name = req.params.get('name')
    # if not name:
    #     try:
    #         req_body = req.get_json()
    #     except ValueError:
    #         pass
    #     else:
    #         name = req_body.get('name')

    # if name:
    #     return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    # else:
    #     return func.HttpResponse(
    #          "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
    #          status_code=200
    #     )