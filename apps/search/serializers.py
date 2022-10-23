from rest_framework import serializers

from apps.search.models import GeneralizedHitsSearch


class GeneralizedHitsSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralizedHitsSearch
        fields = ('source', 'source_id', 'title', 'description', 'doi', 'type', 'language', 'publication_date',
                  'original_url', 'access_right', 'citations_number')
