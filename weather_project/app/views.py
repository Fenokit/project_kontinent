from django.shortcuts import render
# from translate import Translator
import datetime
import requests
import json


# Create your views here.
def weather(request, lat='55.75396', lot='37.620393'):
    # translator = Translator(to_lang="ru")

    api_key = '965e9718-92ee-4d4a-90f4-a1ba57554fd3'
    url = f'https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lot}&lang=ru_RU'
    headers = {'X-Yandex-API-Key': api_key}
    try:
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)

        sunrise = datetime.datetime.strptime(data['forecasts'][0]['sunrise'], '%H:%M')
        sunset = datetime.datetime.strptime(data['forecasts'][0]['sunset'], '%H:%M')
        duration_of_the_day = sunset - sunrise
        condition = data['fact']['condition']
        print(f"{condition} - {data['fact']['condition']}")
        print(data['forecasts'][0])
        weather_to_the_city = {
            'time': data['forecasts'][0]['date'],
            'city': data['geo_object']['locality']['name'],
            'condition': condition,
            'temperature': data['fact']['temp'],
            'icon': f"static/icons/{data['fact']['icon']}.svg",
            'link': data['info']['url'],

            'humidity': data['fact']['humidity'],
            'pressure': data['fact']['pressure_pa'],
            'wind': data['fact']['wind_speed'],

            'sunrise_timestamp': data['forecasts'][0]['sunrise'],
            'sunset_timestamp': data['forecasts'][0]['sunset'],
            'duration_of_the_day': duration_of_the_day,
        }

        return render(request, 'weather/index.html', weather_to_the_city)
    except Exception as ex:
        print(ex)
        return
