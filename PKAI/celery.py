import os
from celery import Celery, shared_task
from celery.schedules import crontab
from celery.utils.log import get_task_logger

# from apps.site.news.tasks import collect_news

logger = get_task_logger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PKAI.settings')

app = Celery('quick_publisher')
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'collect_news': {
        'task': 'apps.site.news.tasks.collect_news',
        'schedule': crontab(minute=0, hour=0),
    },
    'remove_old_hits': {
        'task': 'apps.search.tasks.remove_old_hits',
        'schedule': crontab(minute='*/10')
    },
}

