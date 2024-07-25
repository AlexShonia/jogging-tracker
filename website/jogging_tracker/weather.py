import requests, datetime
from django.conf import settings
from rest_framework.exceptions import ValidationError


def get_weather(serializer):
    api_key = settings.WEATHER_API_KEY

    date = serializer.validated_data.get("date")
    city_name = serializer.validated_data.get("location")

    timestamp = int(
        datetime.datetime.combine(date, datetime.datetime.min.time()).timestamp()
    )

    base_url = settings.WEATHER_URL
    geo_url = f"{base_url}/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
    geo_response = requests.get(geo_url)
    geo = geo_response.json()

    if len(geo) == 0:
        raise ValidationError("City not found")

    lat = geo[0].get("lat")
    lon = geo[0].get("lon")

    weather_url = f"{base_url}/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={timestamp}&units=metric&appid={api_key}"
    weather_response = requests.get(weather_url)
    weather_json = weather_response.json()

    if not weather_json["data"]:
        raise ValidationError("Something went wrong")

    temperature = int(weather_json["data"][0]["temp"])
    weather_description = weather_json["data"][0]["weather"][0]["description"]

    return {
        "temperature": temperature,
        "description": weather_description,
    }
