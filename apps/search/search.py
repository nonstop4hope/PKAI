# from typing import List
#
# from django.conf import settings
#
# from apps.search.models import ApiResponse, GeneralizedHit
#
#
# class Search:
#     def __init__(self):
#         self.zenodo_access_token = settings.ZENODO_ACCESS_TOKEN
#         self.size = 100
#
#     def _zenodo_request(self, page: int, query: str) -> grequests.AsyncRequest:
#         """ create async request to zenodo """
#         params = {'q': query,
#                   'access_token': self.zenodo_access_token,
#                   'page': page}
#         return grequests.get('https://zenodo.org/api/records', params=params)
#
#     def _parse_one_zenodo_hit(self, response_json) -> GeneralizedHit:  # TODO: set input type
#         """ parse one json to generalized model """
#         pass
#
#     def _parse_zenodo_response(self, response) -> List[GeneralizedHit]:  # TODO: set response type
#         """ parse zenodo response to generalized model """
#         pass
#
#     def _get_zenodo_records_by_query_async(self, search_query: str, page_num: int = 5) -> ApiResponse:
#         """ get records on request """
#         zenodo_response = ApiResponse()
#         api_requests = (self._zenodo_request(page=page, query=search_query) for page in range(1, page_num + 1))
#         api_responses = grequests.map(api_requests)
#         for api_response in api_responses:
#             pass
#         return zenodo_response
