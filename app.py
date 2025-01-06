from flask import Flask, render_template, request, jsonify
import requests
import os
#import datetime

from dotenv import load_dotenv
load_dotenv()

#import coordinate

app = Flask(__name__)

AZURE_FUNCTION_URL = "https://weatheralertfunctionapp.azurewebsites.net/api/SendWeatherAlert"
API_KEY = os.getenv("openweather_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather" 

@app.route("/") #, methods=["GET", "POST"]
def home():
    return render_template('index.html')
    # weather_data = None
    # error = None
    # city = None
    # dt_object = None

    # if request.method == "POST":
    #     city = request.form.get("city")
    #     if city:
            
    #         try:
    #             coordinates = coordinate.get_coordinates(city)
    #             response = requests.get(BASE_URL, params={"lat": coordinates[0],"lon": coordinates[1],"units": "metric","appid": API_KEY})
    #             response.raise_for_status()
    #             weather_data = response.json()
    #             dt = weather_data['dt']
    #             dt_object = datetime.datetime.fromtimestamp(dt)
    #         except requests.exceptions.HTTPError as e:  
    #             error = f"City not found or an error occurred: {e}"
    #     else:
    #         error = "Please enter a city name."

    # return render_template("index.html", weather_data=weather_data, city=city,dt_object=dt_object , error=error)

@app.route('/trigger-alert', methods=['POST'])
def trigger_alert():
    city = request.form.get('city')
    threshold_temp = request.form.get('threshold_temp')
    
    try:
        response = requests.get(
            AZURE_FUNCTION_URL,
            params={
                'city': city,
                'threshold_temp': threshold_temp
            }
        )
        response.raise_for_status()
        try:
            data = response.json()
            return jsonify({"status": "success", "message": data['message']}['message'])
        except ValueError as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
