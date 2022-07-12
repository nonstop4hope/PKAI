from django.db import models


class FavoriteRecord(models.Model):
    user = models.IntegerField(blank=False)
    record_id = models.IntegerField(blank=False)
