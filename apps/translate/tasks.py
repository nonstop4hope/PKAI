from celery import shared_task
from celery.utils.log import get_task_logger

from apps.translate.models import Translation
from apps.translate.translators.translators_server import TranslatorsServer

logger = get_task_logger(__name__)


@shared_task(name='translate')
def async_translate(source_text: str, to_language: str = 'ru') -> str:
    tss = TranslatorsServer()
    return tss.translate_html(html_text=source_text, to_language=to_language)
