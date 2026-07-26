from rest_framework.viewsets import ModelViewSet
from django.db.models import Q

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        return queryset


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    def get_queryset(self):
        queryset = Stock.objects.all()
        products = self.request.query_params.get('products')
        if products:
            queryset = queryset.filter(positions__product_id=products)
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(positions__product__title__icontains=search)
        return queryset.distinct()
