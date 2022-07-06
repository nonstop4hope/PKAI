import dataclasses
import time
from typing import Dict

from celery import shared_task
from celery.utils.log import get_task_logger

from apps.search.zenodo.zenodo import ZenodoAPI

logger = get_task_logger(__name__)


@shared_task(name='get_zenodo_records')
def get_zenodo_records_async(search_query: str, page: int) -> Dict:
    zenodo_api = ZenodoAPI()
    logger.info('Getting zenodo response by query %s and page %s', search_query, page)
    return dataclasses.asdict(zenodo_api.get_records_by_query(search_query, page))
