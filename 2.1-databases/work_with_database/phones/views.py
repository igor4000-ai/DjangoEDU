import csv
from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from phones.models import Phone


def import_phones():
    """Импорт телефонов из CSV-файла."""
    csv_path = 'phones.csv'
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            Phone.objects.get_or_create(
                slug=row['id'],
                defaults={
                    'name': row['name'],
                    'image': row['image'],
                    'price': Decimal(row['price']),
                    'release_date': row['release_date'],
                    'lte_exists': row['lte_exists'] == 'True',
                }
            )


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    sort_param = request.GET.get('sort')
    phones = Phone.objects.all()

    if sort_param == 'name':
        phones = phones.order_by('name')
    elif sort_param == 'min_price':
        phones = phones.order_by('price')
    elif sort_param == 'max_price':
        phones = phones.order_by('-price')
    else:
        phones = phones.order_by('id')

    context = {'phones': phones}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone = get_object_or_404(Phone, slug=slug)
    context = {'phone': phone}
    return render(request, template, context)
