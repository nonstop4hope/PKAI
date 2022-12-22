from django.db import models
from django.db.models import CASCADE
from django.contrib.auth.models import User
from apps.site.custom_auth.models import UserData

from apps.search.models import GeneralizedHitsSearch


class FavoriteRecord(models.Model):
    user = models.ForeignKey(UserData, on_delete=CASCADE)
    record = models.ForeignKey(GeneralizedHitsSearch, related_name='favorites', on_delete=CASCADE)
