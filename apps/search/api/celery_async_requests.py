import logging

import requests.models
from celery import shared_task
from celery.result import AsyncResult
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task()
def get(url: str='', timeout: int = 30) -> requests.models.Response:
    # if headers is None:
    #     headers = {}
    resp = requests.get(url='https://catfact.ninja/fact', timeout=timeout)
    logger.info(resp.status_code)
    return resp.json()


@shared_task
def post(url: str, body: dict, headers=None, timeout: int = 30):
    if headers is None:
        headers = {}
    logger.info(url)
    return requests.post(url=url, body=body, headers=headers)
