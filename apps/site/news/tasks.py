import time

from celery import signals, shared_task
from celery.utils.log import get_task_logger

from apps.site.news.collector import NewsCollector

logger = get_task_logger(__name__)


@signals.worker_ready.connect
def collect_news(**kwargs):
    collector = NewsCollector()
    while True:
        collector.collect()
        time.sleep(10*60)
