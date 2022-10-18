import logging

import requests.models
from celery import shared_task
from celery.result import AsyncResult
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task()
def get(url: str, headers: dict = None, timeout: int = 30, params: dict = None) -> requests.models.Response:
    if headers is None:
        headers = {}
    resp = requests.get(url=url, timeout=timeout, headers=headers, params=params)
    return resp.json()


@shared_task
def post(url: str, body=None, headers=None, timeout: int = 30):
    if headers is None:
        headers = {}
    resp = requests.post(url=url, json=body, headers=headers, timeout=timeout)
    logger.info(resp.status_code)
    return resp.json()
