import dataclasses

import redis
from django.http import JsonResponse

from PKAI import settings
from .celery_result import get_task_state_by_id
from .tasks import get_zenodo_records_async
from .zenodo.models import ZenodoResponse


def get_zenodo_records(request):
    search_query = request.GET.get('query')
    page = request.GET.get('page')
    return JsonResponse({'task_id': str(get_zenodo_records_async.delay(search_query, page))})


def get_celery_result_by_id(request):
    task_id = request.GET.get('task_id')
    response = get_task_state_by_id(task_id)
    return JsonResponse(response)


def get_result(request):
    search_query = request.GET.get('query')
    page = request.GET.get('page')
    redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
    records_json = redis_instance.get(f'{search_query}_{page}')
    if records_json is not None:
        response = ZenodoResponse.from_json(records_json)
        return JsonResponse(dataclasses.asdict(response))
