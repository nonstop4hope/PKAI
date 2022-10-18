from celery import shared_task
from celery.utils.log import get_task_logger

from apps.site.news.collector import NewsCollector

logger = get_task_logger(__name__)


@shared_task
def collect_news(**kwargs):
    collector = NewsCollector()
    collector.collect()
