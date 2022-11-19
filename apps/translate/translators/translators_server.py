import os
import re
from typing import Union

import pathos

from apps.translate.translators.exceptions import TranslatorError
from apps.translate.translators.sogou import Sogou


class TranslatorsServer:
    def __init__(self):
        self._sogou = Sogou()
        self.sogou = self._sogou.sogou_api
        self.translators_dict = {
            'sogou': self.sogou,
        }
        self.translators_pool = list(self.translators_dict.keys())

    def translate_text(self,
                       query_text: str,
                       translator: str = 'sogou',
                       from_language: str = 'auto',
                       to_language: str = 'ru',
                       **kwargs
                       ) -> Union[str, dict]:
        """
        :param query_text: str, must.
        :param translator: str, default 'sogou'.
        :param from_language: str, default 'auto'.
        :param to_language: str, default 'ru'.
        :param **kwargs:
                :param if_ignore_limit_of_length: boolean, default False.
                :param is_detail_result: boolean, default False.
                :param timeout: float, default None.
                :param proxies: dict, default None.
                :param sleep_seconds: float, default `random.random()`.
        :return: str or dict
        """
        if translator not in self.translators_pool:
            raise TranslatorError
        return self.translators_dict[translator](query_text=query_text, from_language=from_language,
                                                 to_language=to_language, **kwargs)

    def translate_html(self,
                       html_text: str,
                       translator: str = 'sogou',
                       from_language: str = 'auto',
                       to_language: str = 'ru',
                       n_jobs: int = -1,
                       **kwargs
                       ) -> str:
        """
        Translate the displayed content of html without changing the html structure.
        :param html_text: str, html format.
        :param from_language: str, default 'auto'.
        :param to_language: str, default: 'en'.
        :param translator: str, default 'bing'.
        :param n_jobs: int, default -1, means os.cpu_cnt().
        :param **kwargs:
            :param if_ignore_limit_of_length: boolean, default False.
            :param timeout: float, default None.
            :param proxies: dict, default None.
        :return: str, html format.
        """
        if kwargs:
            for param in ('query_text', 'is_detail_result'):
                if param in kwargs:
                    raise TranslatorError(f'{param} should not be in `**kwargs`.')
        kwargs.update({'sleep_seconds': 0})
        if translator not in self.translators_pool:
            raise TranslatorError

        n_jobs = os.cpu_count() if n_jobs <= 0 else n_jobs
        _ts = self.translators_dict[translator]

        pattern = re.compile(
            r"(?:^|(?<=>))([\s\S]*?)(?:(?=<)|$)")  # TODO: <code></code> <div class="codetext notranslate">
        sentence_list = list(set(pattern.findall(html_text)))
        _map_translate_func = lambda sentence: (
            sentence, _ts(query_text=sentence, from_language=from_language, to_language=to_language, **kwargs))

        with pathos.multiprocessing.ProcessPool(n_jobs) as pool:
            result_list = pool.map(_map_translate_func, sentence_list)

        result_dict = {text: ts_text for text, ts_text in result_list}
        _get_result_func = lambda k: result_dict.get(k.group(1), '')
        return pattern.sub(repl=_get_result_func, string=html_text)
