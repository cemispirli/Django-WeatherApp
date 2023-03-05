from .models import City
from django.shortcuts import get_object_or_404, redirect, render
from decouple import config
import requests
from pprint import pprint
from django.contrib import messages

def home(request):
    API_key = config('API_KEY')
    user_city = request.GET.get('name')
    if user_city:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={user_city}&appid={API_key}&units=metric"
        response = requests.get(url)
        if response.ok:
            content = response.json()
            response_city = content['name']
            if City.objects.filter(name=response_city):
                messages.warning(request, 'City already exists!')
            else:
                City.objects.create(name=response_city)
                messages.success(request, 'City created!')
        else:
            messages.error(request, 'There is no city!')
        return redirect('home')
    
    city_data = []
    cities = City.objects.all().order_by('-id')
    for city in cities:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}&units=metric"
        response = requests.get(url)
        content = response.json()
        data = {
            # 'city': content['name'],
            'city': city,
            'temp': content['main']['temp'],
            'icon' : content['weather'][0]['icon'],
            'desc' : content['weather'][0]['description'],
        }
        city_data.append(data)
        pprint(city_data)
        
    context = {
        'city_data': city_data,
    }
    return render(request, 'weatherapp/home.html', context)

def delete_city(request, id):
    city = get_object_or_404(City, id=id)
    city.delete()
    messages.success(request, 'City deleted!')
    return redirect('home')

