from rest_framework import serializers

from .models import FavoriteRecord


class FavoriteRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteRecord
        fields = ('id', 'record_id',)
