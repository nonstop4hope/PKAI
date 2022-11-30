import logging
from datetime import datetime
from http import HTTPStatus

from django.http import JsonResponse, HttpResponse
from rest_framework import generics, permissions, mixins
from rest_framework.response import Response

from .api import zenodo_citations
from .api.opencitations_api import OpencitationsAPI
from .api.search_api import SearchAPI
from .celery_result import get_task_state_by_id
from .file_downloader import get_file_from_url
from .models import GeneralizedHitsSearch
from .serializers import GeneralizedHitsSearchSerializer, OneHitSerializer
from .tasks import get_core_records_async
from .tasks import get_zenodo_records_async

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


class GeneralizedSearch(generics.ListAPIView):
    serializer_class = GeneralizedHitsSearchSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        query = self.request.query_params['query']
        return GeneralizedHitsSearch.objects.filter(query=query)

    def get(self, request, *args, **kwargs):
        query = self.request.query_params['query']
        if len(GeneralizedHitsSearch.objects.filter(query=query)) == 0:
            search = SearchAPI()
            if 'sort' in self.request.query_params:
                sort = self.request.query_params['sort']
            else:
                sort = None
            search.get_records_by_query_async(search_query=self.request.query_params['query'], sort=sort)
        return self.list(request, *args, **kwargs)


class OneHit(mixins.RetrieveModelMixin, generics.GenericAPIView):
    serializer_class = OneHitSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def retrieve(self, request, *args, **kwargs):
        source_id = self.request.query_params['id']
        source = request.query_params['source']
        opencitations = OpencitationsAPI()
        try:
            instance = GeneralizedHitsSearch.objects.get(source_id=source_id, source=source)
            instance.citations_number = opencitations.get_opencitation_statistic(instance.doi)
        except GeneralizedHitsSearch.DoesNotExist:
            search = SearchAPI()
            if source == 'zenodo':
                search.get_single_zenodo_hit(source_id)
                instance = GeneralizedHitsSearch.objects.get(source_id=source_id, source=source)
            else:
                search.get_single_core_hit(source_id)
                instance = GeneralizedHitsSearch.objects.get(source_id=source_id, source=source)
            instance.citations_number = opencitations.get_opencitation_statistic(instance.doi)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class GetFile(mixins.RetrieveModelMixin, generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        url = request.GET.get('url')
        file = get_file_from_url(url)
        logger.info(file)

        with open(file.path, 'rb') as f:
            file_data = f.read()

        logger.info(file)
        response = HttpResponse(file_data, content_type=file.content_type)
        response['Content-Disposition'] = f'attachment; filename={file.name}'
        return response
