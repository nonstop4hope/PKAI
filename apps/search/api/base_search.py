import logging
import re

from django.conf import settings

# from keybert import KeyBERT
from apps.site.favorite_records.models import FavoriteRecord

logger = logging.getLogger('__name__')


class BaseSearch:
    def __init__(self):
        self.zenodo_access_token = settings.ZENODO_ACCESS_TOKEN
        self.size = 100

    @staticmethod
    def _remove_tags(text):
        """ remove html tags from hit description """
        tag_re = re.compile(r'<[^>]+>')
        return tag_re.sub('', text)
