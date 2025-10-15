from flask import Flask, render_template, request, session
import requests

app = Flask(__name__)

API_KEY = "d95882f9eadd331b022755a55eed0a95"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    
    if request.method == "POST":
        city = request.form.get("city")

        if city:
            params = {
                "q": city,
                "appid": API_KEY,
                "units": "metric"
            }

            response = requests.get(BASE_URL, params=params)

            try:
                if response.status_code == 200:
                    data = response.json()
                    message = (
                        f"Weather in {city} 🌍\n"
                        f"🌡️ Temperature : {data['main']['temp']} °C\n"
                        f"🌨️ Condition : {data['weather'][0]['description'].capitalize()}\n"
                        f"☁ Humidity : {data['main']['humidity']} %\n"
                        f"💨 Wind Speed : {data['wind']['speed']} m/s\n"
                    )
                else:
                    message = "❌ City not found or error in fetching data..."
            except Exception as e:
                message = f"⚠️ Error: {str(e)}"
        else:
            print("Please enter a city name...")

    return render_template("index.html", message=message)


if __name__ == "__main__":
    print("🚀 Starting Flask server...")
    app.run(debug=True)
