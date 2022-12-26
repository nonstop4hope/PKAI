import logging

from django.http import JsonResponse
from rest_framework import generics, permissions

import apps
from apps.search.exceptions import RecordIsNotExists
from apps.search.models import GeneralizedHitsSearch
from apps.site.favorite_records.models import FavoriteRecord
from apps.site.favorite_records.serializers import FavoriteRecordSerializer
from apps.search.serializers import GeneralizedHitsSearchSerializer

logger = logging.getLogger('__name__')


class AddRecordToFavorites(generics.CreateAPIView):
    serializer_class = FavoriteRecordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        record_id = request.data.get('id')
        try:
            record = GeneralizedHitsSearch.objects.get(pk=record_id)
        except GeneralizedHitsSearch.DoesNotExist:
            raise RecordIsNotExists

        favorite, created = FavoriteRecord.objects.get_or_create(user=user, record=record)

        return JsonResponse({
            'created': created,
        })


class ListFavoriteRecords(generics.ListAPIView):
    serializer_class = GeneralizedHitsSearchSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return [favorite.record for favorite in FavoriteRecord.objects.filter(user=user)]


class DeleteFavoriteRecord(generics.DestroyAPIView):
    serializer_class = FavoriteRecordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        user = request.user
        record_id = request.data.get('id')

        try:
            record = FavoriteRecord.objects.get(user=user, record_id=record_id)
            record.delete()
        except FavoriteRecord.DoesNotExist:
            raise RecordIsNotExists

        return JsonResponse({
            'deleted': True,
        })
