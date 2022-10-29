from apps.search.api.core import Core
from apps.search.api.zenodo import Zenodo
from apps.search.models import ApiResponse


class SearchAPI(Core, Zenodo):

    def get_records_by_query_async(self, search_query: str, total_pages: int = 5) -> ApiResponse:

        response = ApiResponse()

        core_api_tasks = self._get_core_async_tasks(query=search_query)
        zenodo_api_tasks = self._get_zenodo_async_tasks(query=search_query, total_pages=total_pages)

        core_api_responses = [core_task.wait(interval=0.1) for core_task in core_api_tasks]
        zenodo_api_responses = [zenodo_task.wait(interval=0.1) for zenodo_task in zenodo_api_tasks]

        for api_response in core_api_responses:
            response.hits += self._get_core_hits(api_response=api_response, query=search_query)

        zenodo_hits = []
        for api_response in zenodo_api_responses:
            zenodo_hits += self._get_zenodo_hits(api_response=api_response, query=search_query)

        response.total_records = len(response.hits)
        return response


