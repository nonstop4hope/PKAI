from rest_framework import serializers

from .models import FavoriteRecord
from ...search.models import GeneralizedHitsSearch
from ...search.serializers import AuthorSerializer, RelatedIdentifierSerializer


class FavoriteRecordsHitSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    related_identifiers = RelatedIdentifierSerializer(many=True)

    class Meta:
        model = GeneralizedHitsSearch
        fields = ('id', 'source', 'source_id', 'title', 'description', 'doi', 'type', 'language', 'publication_date',
                  'original_url', 'access_right', 'citations_number', 'source_keywords', 'authors',
                  'related_identifiers', 'favourite')


class FavoriteRecordSerializer(serializers.ModelSerializer):
    record = FavoriteRecordsHitSerializer(many=False)

    class Meta:
        model = FavoriteRecord
        fields = ('id', 'record')
