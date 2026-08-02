from django_filters import rest_framework as filters

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявления."""

    # TODO: добавьте фильтры по статусу и создателю

    class Meta:
        model = Advertisement
        fields = ['status', 'creator']
