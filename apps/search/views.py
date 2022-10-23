import logging
from http import HTTPStatus

from django.http import JsonResponse
from rest_framework import generics, permissions

from .api.search_api import SearchAPI
from .celery_result import get_task_state_by_id
from .models import GeneralizedHitsSearch
from .serializers import GeneralizedHitsSearchSerializer
from .tasks import get_zenodo_records_async
from .tasks import get_core_records_async

logger = logging.getLogger('__name__')


def get_zenodo_records(request):
    if request.user.is_authenticated:
        search_query = request.GET.get('query')
        page = int(request.GET.get('page', 1))
        return JsonResponse({'task_id': str(get_zenodo_records_async.delay(search_query, page))})
    else:
        return JsonResponse({"detail": "Authentication credentials were not provided."}, status=HTTPStatus.FORBIDDEN)


def get_core_records(request):
    if request.user.is_authenticated:
        search_query = request.GET.get('query')
        page = int(request.GET.get('page', 1))
        core_records = str(get_core_records_async.delay(search_query, page))
        return JsonResponse({'task_id': core_records})
    else:
        return JsonResponse({"detail": "Authentication credentials were not provided."}, status=HTTPStatus.FORBIDDEN)


def get_celery_result_by_id(request):
    if request.user.is_authenticated:
        task_id = request.GET.get('task_id')
        response = get_task_state_by_id(task_id)
        return JsonResponse(response)
    else:
        return JsonResponse({"detail": "Authentication credentials were not provided."}, status=HTTPStatus.FORBIDDEN)


def get_generalized_results(request):
    if request.user.is_authenticated:
        search_query = request.GET.get('query')
        search = SearchAPI()
        response = search.get_records_by_query_async(search_query=search_query)
        return JsonResponse(response.dict(), safe=False)
    else:
        return JsonResponse({"detail": "Authentication credentials were not provided."}, status=HTTPStatus.FORBIDDEN)


class Test(generics.ListAPIView):
    serializer_class = GeneralizedHitsSearchSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        query = self.request.query_params['query']
        return GeneralizedHitsSearch.objects.filter(query=query)

    def get(self, request, *args, **kwargs):
        query = self.request.query_params['query']
        if len(GeneralizedHitsSearch.objects.filter(query=query)) == 0:
            search = SearchAPI()
            search.get_records_by_query_async(search_query=self.request.query_params['query'])
        return self.list(request, *args, **kwargs)
