from apps.search.api.core import Core
from apps.search.api.zenodo import Zenodo


class SearchAPI(Core, Zenodo):

    def get_records_by_query_async(self, search_query: str, sort: str, total_pages: int = 5):

        core_api_tasks = self._get_core_async_tasks(query=search_query)
        zenodo_api_tasks = self._get_zenodo_async_tasks(query=search_query, total_pages=total_pages, sort=sort)

        core_api_responses = [core_task.wait(interval=0.5) for core_task in core_api_tasks]
        zenodo_api_responses = [zenodo_task.wait(interval=0.5) for zenodo_task in zenodo_api_tasks]

        for api_response in core_api_responses:
            self._get_core_hits(api_response=api_response)

        for api_response in zenodo_api_responses:
            self._get_zenodo_hits(api_response=api_response)
