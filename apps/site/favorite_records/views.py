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
        record_id = request.POST.get('id')
        try:
            record = GeneralizedHitsSearch.objects.get(pk=record_id)
        except apps.search.models.GeneralizedHitsSearch.DoesNotExist:
            raise RecordIsNotExists
        favorite, created = FavoriteRecord.objects.get_or_create(user=user, record=record)
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



