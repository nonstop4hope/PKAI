import math
import re
from typing import List

import requests
from django.conf import settings

from apps.search.zenodo.models import ZenodoHit, HitCreator, ZenodoResponse


class ZenodoAPI:
    def __init__(self):
        self.access_token = settings.ZENODO_ACCESS_TOKEN
        self.size = 10

    @staticmethod
    def _remove_tags(text):
        """ remove html tags from description zenodo-record """
        tag_re = re.compile(r'<[^>]+>')
        return tag_re.sub('', text)

    def _parse_zenodo_api_response(self, response: requests.models.Response) -> List[ZenodoHit]:
        """ parse zenodo response to dataclass """
        hits: List[ZenodoHit] = []
        for zenodo_hit in response.json()['hits']['hits']:
            hit = ZenodoHit()
            hit.title = zenodo_hit['metadata']['title']
            hit.description = self._remove_tags(zenodo_hit['metadata']['description']).replace('\n', ' ')
            hit.publication_date = zenodo_hit['metadata']['publication_date']
            keywords = []
            try:
                for keyword in zenodo_hit['metadata']['keywords']:
                    keywords.append(keyword)
            except KeyError:
                pass
            hit.keywords = keywords
            hit.link = zenodo_hit['links']['latest_html']
            hit.access_right = zenodo_hit['metadata']['access_right']
            creators = []
            for hit_creator in zenodo_hit['metadata']['creators']:
                creator = HitCreator()
                try:
                    creator.affiliation = hit_creator['affiliation']
                except KeyError:
                    pass
                creator.name = hit_creator['name']
                creators.append(creator)
            hit.creators = creators
            hits.append(hit)
        return hits

    def _get_total_pages_number(self, total_hits: int) -> int:
        """ calculate the total number of pages """
        return math.ceil(total_hits/self.size)

    def get_records_by_query(self, search_query: str, page: int) -> ZenodoResponse:
        """ get records on request """
        zenodo_response = ZenodoResponse()
        resp = requests.get('https://zenodo.org/api/records',
                            params={'q': search_query,
                                    'access_token': self.access_token,
                                    'page': page})
        zenodo_response.records = self._parse_zenodo_api_response(resp)
        zenodo_response.pages_number = self._get_total_pages_number(int(resp.json()['hits']['total']))
        zenodo_response.current_page = page

        return zenodo_response
