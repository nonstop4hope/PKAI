from django.http import JsonResponse
from rest_framework import generics, permissions

from apps.site.favorite_records.models import FavoriteRecord
from apps.site.favorite_records.serializers import FavoriteRecordSerializer


class AddRecordToFavorites(generics.CreateAPIView):

    serializer_class = FavoriteRecordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user.id
        record_id = request.POST.get('record_id')
        favorite, created = self.model.objects.get_or_create(user=user, record_id=record_id)
        return JsonResponse({
            'user': user,
            'record_id': record_id,
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



