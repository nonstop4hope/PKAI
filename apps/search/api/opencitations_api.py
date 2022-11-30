import requests


class OpencitationsAPI:
    def __init__(self):
        self.url = 'https://opencitations.net/index/api/v1/references/'

    @staticmethod
    def _parse_opencitations_response(opencitations_json) -> int:
        #
        # for citation_hits in opencitations_json:
        #     citations.doi_list.append(citation_hits['cited'].replace('coci => ', ''))
        # citations.number = len(citations.doi_list)
        return len(opencitations_json)

    def get_opencitation_statistic(self, doi: str) -> int:
        response = requests.get(f'{self.url}{doi}')
        if doi is not None and len(response.text) > 0:
            return self._parse_opencitations_response(response.json())
        else:
            return 0
