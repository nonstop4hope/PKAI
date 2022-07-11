from django.db import models


class News(models.Model):
    title = models.CharField(blank=False, max_length=512)
    description = models.TextField(blank=True, null=True)
    body = models.TextField(blank=False)
    author = models.CharField(blank=True, null=True, max_length=256)
    publication_date = models.DateTimeField(blank=False)

    def __str__(self):
        return self.title
