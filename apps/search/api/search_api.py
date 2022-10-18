from apps.search.api.core import Core
# from apps.search.api.zenodo import Zenodo
from apps.search.api.zenodo import Zenodo
from apps.search.models import ApiResponse


class SearchAPI(Core, Zenodo):

    # def get_zenodo_records_by_query_async(self, search_query: str, page_num: int = 5) -> ApiResponse:
    #     """ get records on request """
    #     response = ApiResponse()
    #     api_requests = (self._zenodo_async_request(page=page, query=search_query) for page in range(1, page_num + 1))
    #     api_responses = grequests.map(api_requests)
    #     for api_response in api_responses:
    #         response.hits += self._get_zenodo_hits(api_response=api_response)
    #     response.total_records = len(response.hits)
    #     return response

    def get_core_records_by_query_async(self, search_query: str, total_pages: int = 5) -> ApiResponse:
        response = ApiResponse()
        api_responses = self._get_core_async_responses(query=search_query, total_pages=total_pages)
        # api_requests = (self._core_async_requests(page=page, query=search_query) for page in range(1, page_num + 1))
        # api_responses = grequests.map(api_requests)
        for api_response in api_responses:
            response.hits += self._get_core_hits(api_response=api_response)
        response.total_records = len(response.hits)
        return response

    def get_zenodo_records_by_q(self, search_query, total_pages: int = 5):
        response = ApiResponse()
        api_resp = self._get_zenodo_async_responses(query=search_query, total_pages=total_pages)
        for api_r in api_resp:
            response.hits += self._get_zenodo_hits(api_response=api_r)
        response.total_records = len(response.hits)
        return response