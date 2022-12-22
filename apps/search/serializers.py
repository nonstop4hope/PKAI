from rest_framework import serializers

from apps.search.models import GeneralizedHitsSearch, HitAuthor, File, RelatedIdentifier
from apps.site.favorite_records.models import FavoriteRecord


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


class OneHitSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    files = FileSerializer(many=True)
    related_identifiers = RelatedIdentifierSerializer(many=True)
    favourite = serializers.SerializerMethodField()

    def get_favourite(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        if hasattr(obj, "id"):
            id = obj.id
        else:
            id = obj.get('id')
        try:
            FavoriteRecord.objects.get(user=user, record_id=id)
        except FavoriteRecord.DoesNotExist:
            return False

        return True

    class Meta:
        model = GeneralizedHitsSearch
        fields = ('id', 'source_id', 'title', 'description', 'doi', 'type', 'language', 'publication_date',
                  'original_url', 'access_right', 'citations_number', 'source_keywords', 'authors', 'full_text',
                  'favourite', 'related_identifiers', 'files')


class GeneralizedHitsSearchSerializer(OneHitSerializer):

    class Meta:
        model = GeneralizedHitsSearch
        fields = ('id', 'source', 'source_id', 'title', 'description', 'doi', 'type', 'language', 'publication_date',
                  'original_url', 'access_right', 'citations_number', 'source_keywords', 'authors',
                  'related_identifiers', 'favourite')
