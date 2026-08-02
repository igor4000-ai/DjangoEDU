from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement, AdvertisementStatusChoices


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', 'updated_at')

    def create(self, validated_data):
        """Переопределяем создание объявления"""

        # Проверяем, что пользователь авторизован
        # Это предотвращает попытку создания от имени null-пользователя
        user = self.context["request"].user
        if not user.is_authenticated:
            raise serializers.ValidationError(
                "Создание объявлений возможно только для авторизованных пользователей."
            )
        # Мы гарантируем, что создателем объявления будет именно тот пользователь,
        # который его создаёт, а не тот, кого передадут через API.
        # Это предотвращает создание объявлений от чужого имени через API.
        validated_data["creator"] = user
        return super().create(validated_data)

    def validate(self, data):
        """Проверка целостности данных. Проверяем, что у пользователя есть и больше не станет больше 10 открытых объявлений."""
        request = self.context['request']
        user = request.user

        if user.is_authenticated:
            open_count = Advertisement.objects.filter(
                creator=user,
                status=AdvertisementStatusChoices.OPEN
            ).count()

            # При создании нового объявления проверяем лимит
            if self.instance is None and data.get('status', AdvertisementStatusChoices.OPEN) == AdvertisementStatusChoices.OPEN:
                if open_count >= 10:
                    raise serializers.ValidationError(
                        'У вас уже есть 10 открытых объявлений.'
                    )

        return data
