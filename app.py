from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("openweather_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@app.route("/", methods=["GET", "POST"])
def home():
    weather_data = None
    error = None

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            try:
                response = requests.get(BASE_URL, params={"q": city, "appid": API_KEY, "units": "metric"})
                response.raise_for_status()
                weather_data = response.json()
            except requests.exceptions.HTTPError as e:
                error = f"City not found or an error occurred: {e}"
        else:
            error = "Please enter a city name."

    return render_template("index.html", weather_data=weather_data, error=error)

if __name__ == "__main__":
    app.run(debug=True)
