import re
from typing import List

import requests
from django.conf import settings

from apps.search.core.models import CoreHit, HitCreator, CoreResponse


class CoreAPI:
    def __init__(self):
        self.access_token = settings.CORE_ACCESS_TOKEN
        self.size = 100

    @staticmethod
    def _remove_tags(text):
        """ remove html tags from description zenodo-record """
        tag_re = re.compile(r'<[^>]+>')
        return tag_re.sub('', text)

    def _parse_response(self, response: requests.models.Response) -> List[CoreHit]:
        """ parse Core response to dataclass """
        hits: List[CoreHit] = []
        for core_hit in response.json()['results']:
            hit = CoreHit()
            hit.title = core_hit['title']

            if core_hit['abstract'] is not None:
                hit.description = self._remove_tags(core_hit['abstract']).replace('\n', ' ')
            else:
                hit.description = ''

            hit.publication_date = core_hit['publishedDate']
            display_links = list(filter(lambda x: x['type'] == 'display', core_hit['links']))
            if display_links:
                hit.link = display_links[0]['url']
            creators = []
            for hit_creator in core_hit['authors']:
                creator = HitCreator()
                creator.name = hit_creator['name']
                creators.append(creator)
            hit.creators = creators
            hits.append(hit)
        return hits

    def get_records_by_query(self, search_query: str, page: int, records_per_query: int = 10) -> CoreResponse:
        """ get records on request """
        response = CoreResponse()
        api_response = requests.post('https://api.core.ac.uk/v3/search/works',
                                     headers={'Authorization': f'Bearer {self.access_token}'},
                                     json={'q': search_query,
                                           'offset': (page - 1) * records_per_query,
                                           'limit': records_per_query})
        response.records = self._parse_response(api_response)
        response.total_records = int(api_response.json()['totalHits'])
        response.current_page = page
        return response

