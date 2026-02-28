import requests

CITY_MAP = {
    "Pune": (18.52, 73.85),
    "Mumbai": (19.07, 72.87),
    "Delhi": (28.61, 77.20),
    "Bangalore": (12.97, 77.59)
}

def get_weather(city="Pune"):
    lat, lon = CITY_MAP.get(city, CITY_MAP["Pune"])

    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&current_weather=true"
    )

    response = requests.get(url)
    data = response.json()

    return {
        "city": city,
        "temp": data["current_weather"]["temperature"],
        "wind": data["current_weather"]["windspeed"]
    }
