from rest_framework import generics
from measurement.models import Sensor, Measurement
from measurement.serializers import (
    SensorSerializer,
    SensorDetailSerializer,
    MeasurementSerializer,
)


class SensorListView(generics.ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class SensorDetailView(generics.RetrieveUpdateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer


class MeasurementListView(generics.ListCreateAPIView):
    serializer_class = MeasurementSerializer

    def get_queryset(self):
        sensor_id = self.request.query_params.get('sensor')
        if sensor_id:
            return Measurement.objects.filter(sensor_id=sensor_id)
        return Measurement.objects.all()
