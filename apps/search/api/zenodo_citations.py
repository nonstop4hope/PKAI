from typing import List

from apps.search.api import celery_async_requests
from apps.search.models import GeneralizedHitsSearch


def _get_zenodo_citations_async_tasks(doi_list: List[str]):
    async_tasks = [
        celery_async_requests.get.delay(f'https://zenodo-broker.web.cern.ch/api/relationships?page=1&size=10&group_by'
                                        f'=version&id={doi}&relation=isCitedBy&scheme=doi') for doi in doi_list]
    return [async_task.wait(interval=0.1) for async_task in async_tasks]


def add_zenodo_citations(query: str) -> None:
    hits = GeneralizedHitsSearch.objects.filter(query=query, source='zenodo')
    doi_list = [hit.doi for hit in hits]
    responses = _get_zenodo_citations_async_tasks(doi_list)
    for doi, response in zip(doi_list, responses):
        GeneralizedHitsSearch.objects.filter(doi=doi).update(citations_number=response['hits']['total'])
    # return [response['hits']['total'] for response in responses]
