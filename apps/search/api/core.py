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


class Core(BaseSearch):

    def __init__(self):
        super().__init__()
        self.access_token = settings.CORE_ACCESS_TOKEN
        self.size = 50
        self.headers = {'Authorization': f'Bearer {self.access_token}'}

    def _get_core_async_tasks(self, query: str, records_per_query: int = 50):
        async_tasks = []
        body = {'q': query,
                'offset': 0,
                'limit': records_per_query}
        async_tasks.append(celery_async_requests.post.delay(url='https://api.core.ac.uk/v3/search/works',
                                                            headers=self.headers, body=body))

        return async_tasks

    def _request_to_single_core_hit(self, hit_id: str) -> dict:
        response = requests.get(f'https://api.core.ac.uk/v3/works/{hit_id}', headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise RecordIsNotExists

    def _parse_one_core_hit(self, hit_json) -> GeneralizedHitsSearch:

        source = 'core'
        source_id = hit_json['id']

        try:
            return GeneralizedHitsSearch.objects.get(source=source, source_id=source_id)
        except GeneralizedHitsSearch.DoesNotExist:
            pass

        hit = GeneralizedHitsSearch()

        hit.source = source
        hit.source_id = source_id
        hit.title = hit_json['title']

        if hit_json['abstract'] is not None:
            hit.description = self._remove_tags(hit_json['abstract']).replace('\n', ' ')

        if hit_json['fullText'] is not None:
            hit.full_text = hit_json['fullText'].replace("\x00", "\uFFFD")

        hit.publication_date = hit_json['publishedDate']
        display_links = list(filter(lambda x: x['type'] == 'display', hit_json['links']))

        if display_links is not None:
            hit.original_url = display_links[0]['url']

        if hit_json['doi'] is not None:
            hit.doi = hit_json['doi']

        hit.access_right = 'open'
        if hit_json['language'] is not None:
            hit.language = hit_json['language']['code']

        if hit_json['citationCount'] is not None:
            hit.citations_number = hit_json['citationCount']

        if len(hit_json['documentType']) > 0:
            hit.type = hit_json['documentType']

        hit.save()

        for journal in hit_json['journals']:
            for item in journal['identifiers']:
                try:
                    scheme, identifier = item.split(':')
                except ValueError:
                    scheme = 'issn'
                    identifier = item
                identifier, _ = RelatedIdentifier.objects.get_or_create(scheme=scheme, identifier=identifier)
                hit.related_identifiers.add(identifier)

        for hit_author in hit_json['authors']:
            author, _ = HitAuthor.objects.get_or_create(name=hit_author['name'])
            hit.authors.add(author)

        for hit_file in hit_json['sourceFulltextUrls']:
            file, _ = File.objects.get_or_create(hit=hit, key=hit_json['title'], link=hit_file)

        hit.save()

        return hit

    def _get_core_hits(self, api_response: dict) -> List[GeneralizedHitsSearch]:
        if 'results' not in api_response:
            raise TooManyRequests
        return [self._parse_one_core_hit(hit_json=core_hit) for core_hit in api_response['results']]

    def get_single_core_hit(self, hit_id) -> GeneralizedHitsSearch:
        return self._parse_one_core_hit(hit_json=self._request_to_single_core_hit(hit_id))
