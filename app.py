from flask import Flask, render_template, request
import os
import requests

app = Flask(__name__)

API_KEY = os.environ.get("OPENWEATHER_API_KEY", "d95882f9eadd331b022755a55eed0a95")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None

    if request.method == "POST":
        city = request.form.get("city")
        lat = request.form.get("lat")
        lon = request.form.get("lon")

        params = {
            "appid": API_KEY,
            "units": "metric"
        }

        # Use coordinates if provided, otherwise use city name
        if lat and lon:
            params["lat"] = lat
            params["lon"] = lon
        elif city:
            params["q"] = city
        else:
            weather_data = {"error": "Please enter a city or enable location"}
            return render_template("index.html", weather=weather_data)

        try:
            response = requests.get(BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            weather_data = {
                "city": data["name"],
                "temp": int(data["main"]["temp"]),
                "feels_like": int(data["main"]["feels_like"]),
                "humidity": data["main"]["humidity"],
                "wind": int(data["wind"]["speed"]),
                "condition": data["weather"][0]["main"],
                "icon": data["weather"][0]["icon"]
            }
        except requests.exceptions.RequestException as e:
            print(f"Weather API request failed: {e}")
            weather_data = {"error": "Unable to retrieve weather data. Check your internet connection or try again later."}
        except ValueError:
            weather_data = {"error": "Invalid response from weather service."}

    return render_template("index.html", weather=weather_data)

if __name__ == "__main__":
    app.run(debug=True)


