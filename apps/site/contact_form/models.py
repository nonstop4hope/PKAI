from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class FeedbackRecord(models.Model):
    username = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = PhoneNumberField(blank=True, null=True, unique=False)
    message = models.CharField(max_length=2000)
