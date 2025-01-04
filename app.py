from flask import Flask, render_template, request
import requests
import os
import datetime

from dotenv import load_dotenv
load_dotenv()

import coordinate

app = Flask(__name__)

API_KEY = os.getenv("openweather_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather" #"https://api.openweathermap.org/data/2.5/weather"

@app.route("/", methods=["GET", "POST"])
def home():
    weather_data = None
    error = None

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            
            try:
                coordinates = coordinate.get_coordinates(city)
                response = requests.get(BASE_URL, params={"lat": coordinates[0],"lon": coordinates[1],"units": "metric","appid": API_KEY}) #, "units": "metric"
                response.raise_for_status()
                weather_data = response.json()
                dt = weather_data['dt']
                dt_object = datetime.datetime.fromtimestamp(dt)
            except requests.exceptions.HTTPError as e:  
                error = f"City not found or an error occurred: {e}"
        else:
            error = "Please enter a city name."

    return render_template("index.html", weather_data=weather_data, city=city, dt_object=dt_object, error=error)

if __name__ == "__main__":
    app.run(debug=True)
