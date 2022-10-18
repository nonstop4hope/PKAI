# from typing import List
#
# import grequests
#
# from apps.search.models import CitationsShort
#
#
# class OpencitationsAPI:
#     def __init__(self):
#         self.url = 'https://opencitations.net/index/api/v1/references/'
#
#     @staticmethod
#     def _parse_opencitations_response(opencitations_json) -> CitationsShort:
#         citations = CitationsShort()
#         for citation_hits in opencitations_json:
#             citations.doi_list.append(citation_hits['cited'].replace('coci => ', ''))
#         citations.number = len(citations.doi_list)
#         return citations
#
#     def get_citations_async(self, doi_list: List[str]) -> List[CitationsShort]:
#         citations_list = []
#         async_opencitations_requests = (grequests.get(f'{self.url}{doi}')
#                                         for doi in doi_list)
#         opencitations_responses = grequests.map(async_opencitations_requests)
#         for a in opencitations_responses:
#             citations_list.append(self._parse_opencitations_response(a.json()))
#         return citations_list
