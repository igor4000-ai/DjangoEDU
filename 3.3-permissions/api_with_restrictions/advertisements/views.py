from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement
from django_filters.rest_framework import DjangoFilterBackend


class IsOwnerOrAdmin(BasePermission):
    """Разрешение: только автор объявления или админ."""

    def has_permission(self, request, view):
        # Админы имеют доступ ко всему
        if request.user and request.user.is_superuser:
            return True
        # Для чтения (list, retrieve) доступ всем
        if view.action in ['list', 'retrieve']:
            return True
        # Для write-операций нужна аутентификация
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Админы могут делать всё
        if request.user and request.user.is_superuser:
            return True
        # Автор может менять и удалять своё объявление
        return obj.creator == request.user


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для работы с объявлениями."""

    # TODO: настроить права доступа ViewSet, проверяя что пользователь является создателем объявления,
    #   либо является админом

    queryset = Advertisement.objects.all()
    serializer_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdvertisementFilter

    def get_serializer_class(self):
        from advertisements.serializers import AdvertisementSerializer
        return AdvertisementSerializer

    def get_queryset(self):
        queryset = Advertisement.objects.all()
        # Фильтр по создателю
        creator_id = self.request.query_params.get('creator')
        if creator_id:
            queryset = queryset.filter(creator_id=creator_id)
        return queryset

    def get_permissions(self):
        """Возвращает список прав для данного метода."""
        if self.action in ["create", "update", "partial_update"]:
            return [IsAuthenticated()]
        if self.action == "destroy":
            return [IsOwnerOrAdmin()]
        return []
