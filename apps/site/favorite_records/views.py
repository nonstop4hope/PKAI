import logging

from django.http import JsonResponse
from rest_framework import generics, permissions

import apps
from apps.search.exceptions import RecordIsNotExists
from apps.search.models import GeneralizedHitsSearch
from apps.site.favorite_records.models import FavoriteRecord
from apps.site.favorite_records.serializers import FavoriteRecordSerializer

logger = logging.getLogger('__name__')


class AddRecordToFavorites(generics.CreateAPIView):
    serializer_class = FavoriteRecordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user.id
        record_id = request.data.get('id')
        try:
            record = GeneralizedHitsSearch.objects.get(pk=record_id)
        except apps.search.models.GeneralizedHitsSearch.DoesNotExist:
            raise RecordIsNotExists

        favorite, created = FavoriteRecord.objects.get_or_create(user=user, record=record)

        if created:
            record.favourite = True
            record.save()

        return JsonResponse({
            'created': created,
        })


class ListFavoriteRecords(generics.ListAPIView):
    serializer_class = FavoriteRecordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user.id
        return FavoriteRecord.objects.filter(user=user)


class DeleteFavoriteRecord(generics.DestroyAPIView):
    serializer_class = FavoriteRecordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user.id
        return FavoriteRecord.objects.filter(user=user)

    def delete(self, request, *args, **kwargs):
        user = request.user.id
        record_id = request.data.get('id')

        records = FavoriteRecord.objects.filter(user=user)
        all_ids = [record.record.id for record in records]

        if record_id not in all_ids:
            raise RecordIsNotExists

        for record in records:
            if record.record.id == record_id:
                record.delete()
                break

        record = GeneralizedHitsSearch.objects.get(pk=record_id)
        record.favourite = False
        record.save()

        return JsonResponse({
            'deleted': True,
        })
