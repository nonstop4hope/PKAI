from typing import NamedTuple, List

import requests
import user_agent
from bs4 import BeautifulSoup
from celery.utils.log import get_task_logger

from PKAI.settings import SOURCE_NEWS_URL
from apps.site.news.models import News

logger = get_task_logger(__name__)


class Payload(NamedTuple):
    start: int = 0
    limit: int = 15
    lang: str = '_r'
    year: str = '&'
    month: str = ''


class OneNewsPayload(NamedTuple):
    lang: str = '_r'
    year: str = ''
    month: str = ''
    goId: str = ''


class NewsCollector:

    @staticmethod
    def get_last_news() -> List[News]:

        headers = {'User-Agent': user_agent.generate_user_agent()}
        resp = requests.post(SOURCE_NEWS_URL, params={'mod': 'evt_data'}, data=Payload()._asdict(), headers=headers,
                             allow_redirects=False)

        result = []
        for source_news in resp.json()['root']:
            news = News()
            news.title = source_news['heading_r']
            news.author = source_news['country_name_r']
            news.publication_date = source_news['post_date']
            result.append(news)

        return result

    @staticmethod
    def get_news_body_by_id(news_id) -> str:

        headers = {'User-Agent': user_agent.generate_user_agent()}
        params = {
            'mod': 'one_evt',
            'id': news_id
        }
        resp = requests.post(SOURCE_NEWS_URL, params=params, data=OneNewsPayload()._asdict(), headers=headers,
                             allow_redirects=False)

        return resp.json()['content_r']

    @staticmethod
    def parse_news_body(body: str) -> str:
        soup = BeautifulSoup(body)
        text = ''
        for div in soup.find_all('div'):
            text += f'{div.get_text()}\n'
        return text

    def collect(self) -> None:
        last_news = self.get_last_news()

        for number, news in enumerate(last_news):
            if not News.objects.filter(title=news.title).exists():
                content = self.get_news_body_by_id(number)
                news.body = self.parse_news_body(content)
                news.save()
