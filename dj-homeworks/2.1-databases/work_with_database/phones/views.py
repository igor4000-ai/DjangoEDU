from django.shortcuts import render, redirect
from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    
    # Получаем параметр сортировки
    sort_param = request.GET.get('sort')
    
    # Получаем queryset с учетом сортировки
    phones = Phone.objects.all()
    
    if sort_param == 'name':
        phones = phones.order_by('name')
    elif sort_param == 'min_price':
        phones = phones.order_by('price')
    elif sort_param == 'max_price':
        phones = phones.order_by('-price')
    
    context = {
        'phones': phones
    }
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    
    try:
        phone = Phone.objects.get(slug=slug)
    except Phone.DoesNotExist:
        phone = None
    
    context = {
        'phone': phone
    }
    return render(request, template, context)
