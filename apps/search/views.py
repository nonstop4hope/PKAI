import logging
from datetime import datetime, timedelta

from django.http import HttpResponse
from elasticsearch_dsl import Q
from rest_framework import generics, permissions, mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .api.opencitations_api import OpencitationsAPI
from .api.search_api import SearchAPI
from .documents import HitDocument
from .file_downloader import get_file_from_url
from .models import GeneralizedHitsSearch
from .models import QueryHit
from .serializers import GeneralizedHitsSearchSerializer, OneHitSerializer

logger = logging.getLogger('__name__')


class GeneralizedSearch(generics.ListAPIView):
    serializer_class = GeneralizedHitsSearchSerializer
    permission_classes = (permissions.IsAuthenticated,)
    document_class = HitDocument

    def get_queryset(self):
        query = self.request.query_params['query']

        q = Q(
            'multi_match',
            query=query,
            fuzziness='auto')

        search = self.document_class.search().query(q).extra(size=100)
        response = search.execute()
        return response

    def get(self, request, *args, **kwargs):
        query = self.request.query_params['query']
        query_hit, query_was_create = QueryHit.objects.get_or_create(query=query)
        yesterday = datetime.now() - timedelta(days=1)

        if query_was_create or query_hit.creation_date < yesterday:
            search = SearchAPI()
            sort = self.request.query_params.get('sort')
            search.get_records_by_query_async(search_query=query, sort=sort)
            query_hit.creation_date = datetime.now()
            query_hit.save()

        return self.list(request, *args, **kwargs)


class OneHit(mixins.RetrieveModelMixin, generics.GenericAPIView):
    serializer_class = OneHitSerializer
    permission_classes = (permissions.IsAuthenticated,)

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
