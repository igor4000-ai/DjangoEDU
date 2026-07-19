from django.shortcuts import render

from books.models import Book


def books_view(request):
    template = 'books/books_list.html'
    context = {
        'books': Book.objects.all().order_by('pub_date'),
    }
    return render(request, template, context)


def books_by_date(request, pub_date):
    template = 'books/books_list.html'

    previous_date = (
        Book.objects.filter(pub_date__lt=pub_date)
        .order_by('-pub_date')
        .values_list('pub_date', flat=True)
        .first()
    )
    next_date = (
        Book.objects.filter(pub_date__gt=pub_date)
        .order_by('pub_date')
        .values_list('pub_date', flat=True)
        .first()
    )

    context = {
        'books': Book.objects.filter(pub_date=pub_date).order_by('name'),
        'current_date': pub_date,
        'previous_date': previous_date,
        'next_date': next_date,
    }
    return render(request, template, context)
