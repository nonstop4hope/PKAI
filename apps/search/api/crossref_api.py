# from typing import List
#
# import grequests
#
# from apps.search.models import CrossrefInfo, Author
#
#
# class CrossrefAPI:
#     def __init__(self):
#         self.url = 'https://api.crossref.org/works/'
#
#     @staticmethod
#     def _parse_one_crossref_json(response) -> CrossrefInfo:
#         info = CrossrefInfo()
#         info.doi = response['message']['DOI']
#         info.url = response['message']['URL']
#         info.title = response['message']['title'][0]
#         for author_json in response['message']['author']:
#             author = Author()
#             author.name = f'{author_json["given"]} {author_json["family"]}'
#             author.affiliation = author_json['affiliation'][0]['name']
#             info.authors += author
#         return info
#
#     def _crossref_async_request(self, doi: str) -> grequests.AsyncRequest:
#         return grequests.get(f'{self.url}{doi}')
#
#     def _get_crossreff_statistic_async(self, doi_list: List[str]) -> List[CrossrefInfo]:
#         api_requests = (self._crossref_async_request(doi) for doi in doi_list)
#         api_responses = grequests.map(api_requests)
#         return [self._parse_one_crossref_json(response.json()) for response in api_responses]
