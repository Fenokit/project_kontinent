from django.shortcuts import render
from .models import WeatherInformation
import pytz
import datetime
import requests
import json


class WeatherView:
    def __init__(self, request):
        self.request = request

    def get_weather_information(self, lat='55.75396', lot='37.620393'):
        api_key = '965e9718-92ee-4d4a-90f4-a1ba57554fd3'
        url = f'https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lot}&lang=ru_RU'
        headers = {'X-Yandex-API-Key': api_key}

        try:
            response = requests.get(url, headers=headers)
            data = json.loads(response.text)
            timezone = pytz.timezone(data['info']['tzinfo']['name'])
            sunrise = datetime.datetime.strptime(data['forecasts'][0]['sunrise'], '%H:%M')
            sunset = datetime.datetime.strptime(data['forecasts'][0]['sunset'], '%H:%M')
            current_time_utc = datetime.datetime.utcfromtimestamp(data['now']).replace(tzinfo=pytz.utc)
            current_time_local = current_time_utc.astimezone(timezone)

            weather_to_the_city = {
                'time': current_time_local.strftime("%H:%M:%S"),
                'city': data['geo_object']['locality']['name'],
                'condition': data['fact']['condition'],
                'temperature': data['fact']['temp'],
                'icon': f"static/icons/{data['fact']['icon']}.svg",
                'link': data['info']['url'],
                'humidity': data['fact']['humidity'],
                'pressure': data['fact']['pressure_mm'],
                'wind': data['fact']['wind_speed'],
                'sunrise_timestamp': data['forecasts'][0]['sunrise'],
                'sunset_timestamp': data['forecasts'][0]['sunset'],
                'duration_of_the_day': sunset - sunrise,
            }

            self.save_weather_to_database(weather_to_the_city)

            return render(self.request, 'weather/index.html', weather_to_the_city)
        except Exception as ex:
            print(ex)
            return render(self.request, 'weather/error.html')

    def save_weather_to_database(self, weather_data):
        weather_instance = WeatherInformation(
            time=weather_data['time'],
            city=weather_data['city'],
            condition=weather_data['condition'],
            temperature=weather_data['temperature'],
            icon=weather_data['icon'],
            link=weather_data['link'],
            humidity=weather_data['humidity'],
            pressure=weather_data['pressure'],
            wind=weather_data['wind'],
            sunrise_timestamp=weather_data['sunrise_timestamp'],
            sunset_timestamp=weather_data['sunset_timestamp'],
            duration_of_the_day=weather_data['duration_of_the_day']
        )
        weather_instance.save()

def weather(request, lat='55.75396', lot='37.620393'):
    weather_view = WeatherView(request)
    return weather_view.get_weather_information(lat, lot)

