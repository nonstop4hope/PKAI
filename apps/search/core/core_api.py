import json
import re
from typing import List

import requests
from django.conf import settings

from apps.search.models import Hit, HitCreator, ApiResult


class CoreAPI:
    def __init__(self):
        self.access_token = settings.CORE_ACCESS_TOKEN
        self.size = 100

    @staticmethod
    def _remove_tags(text):
        """ remove html tags from description zenodo-record """
        tag_re = re.compile(r'<[^>]+>')
        return tag_re.sub('', text)

    def _get_records(self, data: requests.models.Response) -> List[Hit]:
        """ parse Core response to dataclass """
        hits: List[Hit] = []
        for core_hit in data['results']:
            hit = Hit()
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

    def get_records_by_query(self, search_query: str, page: int, records_per_query: int = 10) -> ApiResult:
        """ get records on request """
        api_result = ApiResult()

        api_response = requests.post('https://api.core.ac.uk/v3/search/works',
                                     headers={'Authorization': f'Bearer {self.access_token}'},
                                     json={'q': search_query,
                                           # 'offset': (page - 1) * records_per_query,
                                           'limit': records_per_query,
                                           'scroll': True})

        json_data = json.loads(api_response.content)

        if api_response.status_code == 200:
            api_result.records = self._get_records(json_data)
            api_result.total_records = int(json_data['totalHits'])
            api_result.current_page = page
        elif api_response.status_code == 500:
            json_data = json.loads(api_response.content)
            api_result.message = json_data['message']

        return api_result

