import logging

from django.http import JsonResponse
from django.views import View

from apps.translate.translators.api import get_translation

logger = logging.getLogger(__name__)


class Translate(View):

    def post(self, request, *args, **kwargs):
        source_text = request.POST.get('text')
        to_language = request.POST.get('to_language')
        if to_language is None:
            to_language = 'ru'
        translation = get_translation(source_text, to_language)
        return JsonResponse(translation.dict())

