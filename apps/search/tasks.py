from datetime import timedelta
from typing import Dict

from celery import shared_task
from celery.utils.log import get_task_logger
from django.db.models.functions import Now

from apps.search.core.core_api import CoreAPI
from apps.search.models import GeneralizedHitsSearch
from apps.search.zenodo.zenodo_api import ZenodoAPI

logger = get_task_logger(__name__)


@shared_task(name='get_zenodo_records')
def get_zenodo_records_async(search_query: str, page: int) -> Dict:
    zenodo_api = ZenodoAPI()
    logger.info('Getting zenodo response by query %s and page %s', search_query, page)

    if page > 1000:
        page = 1000

    records = zenodo_api.get_records_by_query(search_query, page)
    return records.dict()


@shared_task(name='get_core_records')
def get_core_records_async(search_query: str, page: int) -> Dict:
    core_api = CoreAPI()
    logger.info('Getting Core response by query %s and page %s', search_query, page)

    if page > 1000:
        page = 1000

    task_result = core_api.get_records_by_query(search_query, page)
    return task_result.dict()


@shared_task
def remove_old_hits() -> None:
    logger.info(GeneralizedHitsSearch.objects.filter(creation_date__lte=Now() - timedelta(hours=2)).delete())
