from rest_framework import serializers

from .models import FavoriteRecord
from apps.search.serializers import GeneralizedHitsSearchSerializer


class FavoriteRecordSerializer(serializers.ModelSerializer):
    record = GeneralizedHitsSearchSerializer(many=False)

    class Meta:
        model = FavoriteRecord
        fields = ('id', 'record')
