from django.urls import path
from measurement.views import SensorListView, SensorDetailView, MeasurementListView

urlpatterns = [
    path('sensors/', SensorListView.as_view(), name='sensor-list'),
    path('sensors/<int:pk>/', SensorDetailView.as_view(), name='sensor-detail'),
    path('measurements/', MeasurementListView.as_view(), name='measurement-list'),
]
