from django.urls import path
from calculator.views import recipe_view

urlpatterns = [
    path('<str:dish_name>/', recipe_view),
]
