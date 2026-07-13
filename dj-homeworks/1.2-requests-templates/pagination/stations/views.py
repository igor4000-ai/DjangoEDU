from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
import csv
from pagination.settings import BUS_STATION_CSV


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # Читаем CSV файл
    with open(BUS_STATION_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        stations = list(reader)
    
    # Пагинация: 10 станций на страницу
    paginator = Paginator(stations, 10)
    
    # Получаем номер страницы из GET-параметра
    page_number = request.GET.get('page', 1)
    
    # Получаем страницу (если номер некорректный, вернёт последнюю)
    page = paginator.get_page(page_number)
    
    context = {
        'bus_stations': page.object_list,
        'page': page,
    }
    return render(request, 'stations/index.html', context)
