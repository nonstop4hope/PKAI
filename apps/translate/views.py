import logging

from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.views import APIView

from apps.translate.translators.api import get_translation

logger = logging.getLogger(__name__)


class Translate(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        source_text = request.data.get('text')
        to_language = request.data.get('to_language')
        if to_language is None:
            to_language = 'ru'
        translation = get_translation(source_text, to_language)
        return JsonResponse(translation.dict())
