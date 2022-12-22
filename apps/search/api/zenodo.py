import logging
from typing import List

import requests
from django.conf import settings

from apps.search.api import celery_async_requests
from apps.search.api.base_search import BaseSearch
from apps.search.exceptions import TooManyRequests, RecordIsNotExists
from apps.search.models import GeneralizedHitsSearch, HitAuthor, File, RelatedIdentifier

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Zenodo(BaseSearch):

    def __int__(self):
        self.zenodo_access_token: str = settings.ZENODO_ACCESS_TOKEN
        self.size: int = 50

    def _get_zenodo_async_tasks(self, total_pages: int, query: str, sort: str):
        """ create async request to zenodo """
        if sort not in ('bestmatch', 'mostrecent'):
            sort = 'bestmatch'
        async_tasks = []
        for page in range(1, total_pages + 1):
            params = {'q': query,
                      'access_token': self.zenodo_access_token,
                      'page': page,
                      'sort': sort}
            async_tasks.append(celery_async_requests.get.delay(url='https://zenodo.org/api/records', params=params))

        return async_tasks

    @staticmethod
    def _request_to_single_zenodo_hit(hit_id: str) -> dict:
        response = requests.get(f'https://zenodo.org/api/records/{hit_id}')
        if response.status_code == 200:
            return response.json()
        else:
            raise RecordIsNotExists

    def _parse_one_zenodo_hit(self, hit_json) -> GeneralizedHitsSearch:  # TODO: set input type

        source_id = hit_json['id']
        source = 'zenodo'

        try:
            return GeneralizedHitsSearch.objects.get(source=source, source_id=source_id)
        except GeneralizedHitsSearch.DoesNotExist:
            pass

        hit = GeneralizedHitsSearch()
        hit.source = source

        hit.source_id = source_id
        metadata = hit_json['metadata']
        hit.title = metadata['title']

        hit.description = self._remove_tags(metadata['description']).replace('\n', ' ')
        hit.publication_date = metadata['publication_date']

        for keyword in metadata.get('keywords', []):
            hit.source_keywords.append(keyword)

        hit.original_url = hit_json['links']['latest_html']
        hit.access_right = metadata['access_right']
        hit.doi = hit_json['doi']
        hit.language = metadata.get('language')
        hit.type = metadata['resource_type']['type']

        hit.save()

        for related_identifier in metadata.get('related_identifiers', []):
            identifier, _ = RelatedIdentifier.objects.get_or_create(scheme=related_identifier['scheme'],
                                                                    identifier=related_identifier['identifier'])
            hit.related_identifiers.add(identifier)

        for hit_author in metadata['creators']:
            author, _ = HitAuthor.objects.get_or_create(affiliation=hit_author.get('affiliation'),
                                                        name=hit_author['name'])
            hit.authors.add(author)

        for hit_file in hit_json.get('files', []):
            File.objects.get_or_create(hit=hit,
                                       checksum=hit_file['checksum'],
                                       key=hit_file['key'],
                                       link=hit_file['links']['self'],
                                       size=int(hit_file['size']),
                                       type=hit_file['type']
                                       )

        return hit

    def _get_zenodo_hits(self, api_response) -> List[GeneralizedHitsSearch]:
        if 'hits' not in api_response:
            raise TooManyRequests
        return [self._parse_one_zenodo_hit(hit_json=zenodo_hit) for zenodo_hit in api_response['hits']['hits']]

    def get_single_zenodo_hit(self, hit_id) -> GeneralizedHitsSearch:
        return self._parse_one_zenodo_hit(hit_json=self._request_to_single_zenodo_hit(hit_id))
