import dataclasses
import pickle
from typing import Dict

import redis
from celery import shared_task
from celery.utils.log import get_task_logger

from PKAI import settings
from apps.search.zenodo.models import ZenodoResponse
from apps.search.zenodo.zenodo import ZenodoAPI

logger = get_task_logger(__name__)


@shared_task
def cashing_next_zenodo_records(search_query: str, page: str) -> None:
    zenodo_instance = ZenodoAPI()
    redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
    already_cashed_bytes = redis_instance.get(search_query)
    already_cashed = ZenodoResponse()
    if already_cashed_bytes is not None:
        already_cashed = ZenodoResponse.from_json(already_cashed_bytes)
    for cashed_page_number in range(2, int(page) + 5):
        if len(already_cashed.records) <= zenodo_instance.size * cashed_page_number:
            logger.info('Collecting data %s, %s', search_query, page)
            new_records = zenodo_instance.get_records_by_query(search_query, cashed_page_number)
            already_cashed.records += new_records.records
            redis_instance.set(search_query, already_cashed.to_json())


@shared_task(name='get_zenodo_records')
def get_zenodo_records_async(search_query: str, page: int) -> int:
    zenodo_api = ZenodoAPI()
    logger.info('Getting zenodo response by query %s and page %s', search_query, page)
    redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
    records_json = redis_instance.get(search_query)
    if records_json is None:
        records = zenodo_api.get_records_by_query(search_query, 1)
        redis_instance.set(search_query, records.to_json())
        cashing_next_zenodo_records.delay(search_query, page)
    else:
        records = ZenodoResponse.from_json(records_json)
    return records.pages_number



