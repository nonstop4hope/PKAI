from rest_framework import serializers

from .models import FavoriteRecord
from ...search.models import GeneralizedHitsSearch
from ...search.serializers import AuthorSerializer, RelatedIdentifierSerializer


class FavoriteRecordsHitSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    related_identifiers = RelatedIdentifierSerializer(many=True)

    class Meta:
        model = GeneralizedHitsSearch
        fields = ('id', 'title', 'doi', 'type', 'language', 'publication_date', 'authors', 'related_identifiers')


class FavoriteRecordSerializer(serializers.ModelSerializer):
    record = FavoriteRecordsHitSerializer(many=False)

    class Meta:
        model = FavoriteRecord
        fields = ('id', 'record')
