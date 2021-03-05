import requests
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.base import View
from .forms import CityForm
from .models import Weather
from django.db import connection


def get_weather(city):
    key = '499734415c86a89b1da5f47812fe25c7'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&lang=uk&units=metric&appid={key}'
    response = requests.get(url)
    return response.json()


def save_weather(context):
    cursor = connection.cursor()
    if cursor.execute('SELECT * FROM weather_weather WHERE city == %s', [str(context['city'])]):
        cursor.execute('DELETE FROM weather_weather WHERE city == %s', [str(context['city'])])

    Weather.objects.create(city=context['city'], description=context['description'],
                            temperature=context['temp'], wind=context['wind'], image=context['image'])
    # Weather.objects.raw('INSERT INTO TABLE weather_weather VALUES(%s, %s, %f, %f, %s)', [
    #     context['city'], context['description'], context['temp'], context['wind'], context['image']])


def reset_weather(request):
    cursor = connection.cursor()
    cursor.execute('DELETE FROM weather_weather')
    return redirect('/show')


class CityWeather:
    def get_all(self):
        # Weather.objects.get_queryset().order_by('id')
        query = Weather.objects.raw('SELECT * FROM weather_weather ORDER BY -id')
        return query


class GetPageView(View):
    def get(self, request):
        return render(request, 'weather/get_weather.html')

    def post(self, request):
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city'].lower()
            res = get_weather(city)
            if res['cod'] == 200:
                context = {
                    'status': 200,
                    'city': str(city),
                    'description': str(res['weather'][0]['description']),
                    'temp': float(res['main']['temp']),
                    'image': str(res["weather"][0]["icon"]),
                    'wind': float(res['wind']['speed'])
                }
                save_weather(context)
            else:
                context = {
                    'status': 400,
                    'text': 'Даного міста не існує'
                }
        else:
            context = {
                'status': 400,
                'text': 'Некоректні дані'
            }

        return render(request, 'weather/get_weather.html', context)


class FilterCity(CityWeather, ListView):
    paginate_by = 4
    template_name = 'weather/history_page.html'

    def get_queryset(self):
        queryset = Weather.objects.filter(
            city__in=self.request.GET.getlist("city")
        )
        return queryset


class HistoryPage(CityWeather, ListView):
    queryset = Weather.objects.get_queryset().order_by('-id')

    model = Weather
    template_name = 'weather/history_page.html'
    paginate_by = 4
