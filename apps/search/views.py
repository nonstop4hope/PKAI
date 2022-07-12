from django.http import JsonResponse

from .celery_result import get_task_state_by_id
from .tasks import get_zenodo_records_async


def get_zenodo_records(request):
    search_query = request.GET.get('query')
    page = request.GET.get('page')
    return JsonResponse({'task_id': str(get_zenodo_records_async.delay(search_query, page))})


def get_celery_result_by_id(request):
    task_id = request.GET.get('task_id')
    response = get_task_state_by_id(task_id)
    return JsonResponse(response)
