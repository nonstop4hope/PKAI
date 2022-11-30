from django.db import models
from django.db.models import CASCADE

from apps.search.models import GeneralizedHitsSearch


class FavoriteRecord(models.Model):
    user = models.IntegerField(blank=False)
    record = models.OneToOneField(GeneralizedHitsSearch, related_name='record', blank=True, on_delete=CASCADE)
