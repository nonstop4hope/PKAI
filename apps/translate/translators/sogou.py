import hashlib
import re
import random
from typing import Union

import execjs
import requests

from apps.translate.translators.tse import Tse


class Sogou(Tse):
    def __init__(self):
        super().__init__()
        self.host_url = 'https://fanyi.sogou.com'
        self.api_url = 'https://fanyi.sogou.com/api/transpc/text/result'
        self.get_language_url = 'https://dlweb.sogoucdn.com/translate/pc/static/js/app.7016e0df.js'
        self.host_headers = self.get_headers(self.host_url, if_api=False)
        self.api_headers = self.get_headers(self.host_url, if_api=True)
        self.language_map = None
        self.form_data = None
        self.query_count = 0
        self.output_zh = 'zh-CHS'
        self.input_limit = 5000

    def get_language_map(self, ss, get_language_url, timeout, proxies):
        lang_html = ss.get(get_language_url, headers=self.host_headers, timeout=timeout, proxies=proxies).text
        lang_list_str = re.compile('"ALL":\[(.*?)\]').findall(lang_html)[0]
        lang_list = execjs.eval(''.join(['[', lang_list_str, ']']))
        lang_list = [x['lang'] for x in lang_list]
        return {}.fromkeys(lang_list, lang_list)

    def get_form(self, query_text, from_language, to_language):
        uuid = ''
        for i in range(8):
            uuid += hex(int(65536 * (1 + random.random())))[2:][1:]
            if i in range(1, 5):
                uuid += '-'
        sign_text = "" + from_language + to_language + query_text + '109984457'  # window.__INITIAL_STATE__.common.CONFIG.secretCode
        sign = hashlib.md5(sign_text.encode()).hexdigest()
        form = {
            "from": from_language,
            "to": to_language,
            "text": query_text,
            "uuid": uuid,
            "s": sign,
            "client": "pc",  # wap
            "fr": "browser_pc",  # browser_wap
            "needQc": "1",
        }
        return form

    # @Tse.time_stat
    def sogou_api(self, query_text: str, from_language: str = 'auto', to_language: str = 'en', **kwargs) -> Union[str, dict]:
        """
        https://fanyi.sogou.com
        :param query_text: str, must.
        :param from_language: str, default 'auto'.
        :param to_language: str, default 'en'.
        :param **kwargs:
                :param if_ignore_limit_of_length: boolean, default False.
                :param is_detail_result: boolean, default False.
                :param timeout: float, default None.
                :param proxies: dict, default None.
                :param sleep_seconds: float, default `random.random()`.
        :return: str or dict
        """
        is_detail_result = kwargs.get('is_detail_result', False)
        timeout = kwargs.get('timeout', None)
        proxies = kwargs.get('proxies', None)
        # sleep_seconds = kwargs.get('sleep_seconds', random.random())
        if_ignore_limit_of_length = kwargs.get('if_ignore_limit_of_length', False)
        query_text = self.check_query_text(query_text, if_ignore_limit_of_length, limit_of_length=self.input_limit)
        if not query_text:
            return ''

        with requests.Session() as ss:
            _ = ss.get(self.host_url, headers=self.host_headers, timeout=timeout, proxies=proxies).text
            # if not self.get_language_url:
            #     self.get_language_url = 'https:' + re.compile(self.get_language_pattern).search(host_html).group() # TODO
            if not self.language_map:
                self.language_map = self.get_language_map(ss, self.get_language_url, timeout, proxies)

            from_language, to_language = self.check_language(from_language, to_language, self.language_map, output_zh=self.output_zh)
            self.form_data = self.get_form(query_text, from_language, to_language)
            r = ss.post(self.api_url, headers=self.api_headers, data=self.form_data, timeout=timeout, proxies=proxies)
            r.raise_for_status()
            data = r.json()
        # time.sleep(sleep_seconds)
        self.query_count += 1
        return data if is_detail_result else data['data']['translate']['dit']