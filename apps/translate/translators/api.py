from apps.translate.models import Translation
from apps.translate.tasks import async_translate


def get_translation(source_text: str, to_language: str = 'ru') -> Translation:
    translation = Translation()
    translation.source = source_text
    translate_task = async_translate.delay(source_text=source_text, to_language=to_language)
    translation.translate = translate_task.wait(interval=0.5)
    return translation
