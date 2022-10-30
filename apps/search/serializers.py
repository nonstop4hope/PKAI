from rest_framework import serializers

from apps.search.models import GeneralizedHitsSearch, HitAuthor, File, RelatedIdentifier


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = HitAuthor
        fields = ('affiliation', 'name')


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('checksum', 'key', 'link', 'size', 'type', 'creation_date')


class RelatedIdentifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedIdentifier
        fields = ('scheme', 'identifier')


class GeneralizedHitsSearchSerializer(serializers.ModelSerializer):

    authors = AuthorSerializer(many=True)
    related_identifiers = RelatedIdentifierSerializer(many=True)

    class Meta:
        model = GeneralizedHitsSearch
        fields = ('source', 'source_id', 'title', 'description', 'doi', 'type', 'language', 'publication_date',
                  'original_url', 'access_right', 'citations_number', 'source_keywords', 'authors',
                  'related_identifiers')


class OneHitSerializer(serializers.ModelSerializer):

    authors = AuthorSerializer(many=True)
    files = FileSerializer(many=True)
    related_identifiers = RelatedIdentifierSerializer(many=True)

    class Meta:
        model = GeneralizedHitsSearch
        fields = ('source_id', 'title', 'description', 'doi', 'type', 'language', 'publication_date',
                  'original_url', 'access_right', 'citations_number', 'source_keywords', 'authors', 'full_text',
                  'files')
