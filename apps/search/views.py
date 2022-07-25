from http import HTTPStatus

from django.http import JsonResponse

from .celery_result import get_task_state_by_id
from .tasks import get_zenodo_records_async
from .tasks import get_core_records_async


def get_zenodo_records(request):
    if request.user.is_authenticated:
        search_query = request.GET.get('query')
        page = request.GET.get('page')
        return JsonResponse({'task_id': str(get_zenodo_records_async.delay(search_query, page))})
    else:
        return JsonResponse({"detail": "Authentication credentials were not provided."}, status=HTTPStatus.FORBIDDEN)


def get_core_records(request):
    # if request.user.is_authenticated:
    search_query = request.GET.get('query')
    page = request.GET.get('page', 1)
    core_records = str(get_core_records_async.delay(search_query, page))
    return JsonResponse({'task_id': core_records})
    # else:
    #     return JsonResponse({"detail": "Authentication credentials were not provided."}, status=HTTPStatus.FORBIDDEN)


def get_celery_result_by_id(request):
    # if request.user.is_authenticated:
    task_id = request.GET.get('task_id')
    response = get_task_state_by_id(task_id)
    return JsonResponse(response)
    # else:
    #     return JsonResponse({"detail": "Authentication credentials were not provided."}, status=HTTPStatus.FORBIDDEN)
