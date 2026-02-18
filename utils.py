import requests

OPENWEATHER_API_KEY = "59976539a18e7355a1d67b6960c33cab"
VISUALCROSSING_API_KEY = "QEYTLHS7GBLNUMNBANPQUABDG"

# ---------------- CURRENT WEATHER ----------------
def get_current_weather(city):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    )

    try:
        print("API CALL CURRENT WEATHER")
        response = requests.get(url)

        if response.status_code == 404:
            return {"error": "City not found. Please enter valid city name."}

        if response.status_code == 429:
            return {"error": "Too many requests, try after some time."}

        if response.status_code != 200:
            return {"error": "Something went wrong"}

        return response.json()

    except requests.exceptions.RequestException:
        return {"error": "Network error. Please check your internet connection."}


# ---------------- HISTORICAL WEATHER ----------------
def get_historical_weather(city, start_date, end_date):
    url = (
        f"https://weather.visualcrossing.com/VisualCrossingWebServices/"
        f"rest/services/timeline/{city}/{start_date}/{end_date}"
        f"?unitGroup=metric&key={VISUALCROSSING_API_KEY}&contentType=json"
    )

    try:
        print("API CALL HISTORICAL WEATHER")
        response = requests.get(url)

        if response.status_code == 404:
            return {"error": "City not found. Please enter valid city name."}

        if response.status_code == 429:
            return {"error": "Too many requests, try after some time."}

        if response.status_code != 200:
            return {"error": "Error fetching historical data"}

        return response.json()

    except requests.exceptions.RequestException:
        return {"error": "Network error. Please check your internet connection."}


# ---------------- FORECAST WEATHER ----------------
def get_forecast_weather(city):
    url = (
        f"https://api.openweathermap.org/data/2.5/forecast"
        f"?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    )

    try:
        print("API CALL FORECAST WEATHER")
        response = requests.get(url)

        if response.status_code == 404:
            return {"error": "City not found. Please enter valid city name."}

        if response.status_code == 429:
            return {"error": "Too many requests, try after some time."}

        if response.status_code != 200:
            return {"error": "Error fetching forecast data"}

        return response.json()

    except requests.exceptions.RequestException:
        return {"error": "Network error. Please check your internet connection."}


# ---------------- CLEANING FUNCTIONS ----------------
def clean_current_weather(data):
    if "error" in data:
        return data

    return {
        "city": data.get("name"),
        "temp": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "condition": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"]
    }


def clean_historical_weather(data):
    if "error" in data:
        return data

    if "days" not in data:
        return {"error": "No historical data found"}

    cleaned_days = []

    for day in data["days"]:
        cleaned_days.append({
            "date": day["datetime"],
            "temp": day["temp"],
            "humidity": day.get("humidity", "N/A"),
            "conditions": day["conditions"]
        })

    return cleaned_days


def clean_forecast_weather(data):
    if "error" in data:
        return data

    if "list" not in data:
        return {"error": "No forecast data found"}

    forecast_list = []

    for item in data["list"][:10]:
        forecast_list.append({
            "datetime": item["dt_txt"],
            "temp": item["main"]["temp"],
            "humidity": item["main"]["humidity"],
            "condition": item["weather"][0]["description"]
        })

    return forecast_list
