from rest_framework import serializers

from apps.search.models import GeneralizedHitsSearch, HitAuthor, File


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = HitAuthor
        fields = '__all__'


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class GeneralizedHitsSearchSerializer(serializers.ModelSerializer):

    authors = AuthorSerializer(many=True)

    class Meta:
        model = GeneralizedHitsSearch
        fields = ('source', 'source_id', 'title', 'description', 'doi', 'type', 'language', 'publication_date',
                  'original_url', 'access_right', 'citations_number', 'source_keywords', 'authors')


class OneHitSerializer(serializers.ModelSerializer):

    authors = AuthorSerializer(many=True)
    files = FileSerializer(many=True)

    class Meta:
        model = GeneralizedHitsSearch
        fields = ('source_id', 'title', 'description', 'doi', 'type', 'language', 'publication_date',
                  'original_url', 'access_right', 'citations_number', 'source_keywords', 'authors', 'full_text', 'files')
