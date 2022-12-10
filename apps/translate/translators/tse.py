import logging
import urllib

from apps.translate.translators.exceptions import TranslatorError

logger = logging.getLogger(__name__)


class Tse:

    @staticmethod
    def get_headers(host_url, if_api=False, if_referer_for_host=True, if_ajax_for_api=True, if_json_for_api=False):
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
        url_path = urllib.parse.urlparse(host_url).path
        host_headers = {
            'Referer' if if_referer_for_host else 'Host': host_url,
            "User-Agent": user_agent,
        }
        api_headers = {
            'Origin': host_url.split(url_path)[0] if url_path else host_url,
            'Referer': host_url,
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            "User-Agent": user_agent,
        }
        if if_api and not if_ajax_for_api:
            api_headers.pop('X-Requested-With')
            api_headers.update({'Content-Type': 'text/plain'})
        if if_api and if_json_for_api:
            api_headers.update({'Content-Type': 'application/json'})
        return host_headers if not if_api else api_headers

    @staticmethod
    def check_language(from_language, to_language, language_map, output_zh=None, output_auto='auto'):
        auto_pool = ('auto', 'auto-detect')
        zh_pool = ('zh', 'zh-CN', 'zh-CHS', 'zh-Hans', 'zh-Hans_CN', 'cn', 'chi')
        from_language = output_auto if from_language in auto_pool else from_language
        from_language = output_zh if output_zh and from_language in zh_pool else from_language
        to_language = output_zh if output_zh and to_language in zh_pool else to_language

        if from_language != output_auto and from_language not in language_map:
            raise TranslatorError(
                'Unsupported from_language[{}] in {}.'.format(from_language, sorted(language_map.keys())))
        elif to_language not in language_map:
            raise TranslatorError('Unsupported to_language[{}] in {}.'.format(to_language, sorted(language_map.keys())))
        elif from_language != output_auto and to_language not in language_map[from_language]:
            raise TranslatorError('Unsupported translation: from [{0}] to [{1}]!'.format(from_language, to_language))
        elif from_language == to_language:
            raise TranslatorError(f'from_language[{from_language}] and to_language[{to_language}] should not be same.')
        return from_language, to_language

    @staticmethod
    def en_tran(from_lang, to_lang, default_lang='en-US', default_translator='Itranslate'):
        if default_translator in ('Itranslate', 'Lingvanex'):
            from_lang = default_lang if from_lang == 'en' else from_lang
            to_lang = default_lang if to_lang == 'en' else to_lang
            from_lang = default_lang.replace('-', '_') if default_translator == 'Lingvanex' and from_lang[
                                                                                                :3] == 'en-' else from_lang
            to_lang = default_lang.replace('-', '_') if default_translator == 'Lingvanex' and to_lang[
                                                                                              :3] == 'en-' else to_lang
            # warnings.warn(f'Unsupported [language=en] with [{default_translator}]! Please specify it.')
            # warnings.warn(f'default languages: [{from_lang}, {to_lang}]')
        return from_lang, to_lang

    @staticmethod
    def make_temp_language_map(from_language, to_language):
        logger.warning('Did not get a complete language map. And do not use `from_language="auto"`.')
        if not (to_language != 'auto' and from_language != to_language):
            raise TranslatorError("to_language != 'auto' and from_language != to_language")
        lang_list = [from_language, to_language]
        return {}.fromkeys(lang_list, lang_list) if from_language != 'auto' else {from_language: to_language,
                                                                                  to_language: to_language}

    @staticmethod
    def check_query_text(query_text, if_ignore_limit_of_length=False, limit_of_length=5000):
        if not isinstance(query_text, str):
            raise TranslatorError
        query_text = query_text.strip()
        length = len(query_text)
        if length >= limit_of_length and not if_ignore_limit_of_length:
            raise TranslatorError('The length of the text to be translated exceeds the limit.')
        else:
            if length >= limit_of_length:
                logger.warning(
                    f'The translation ignored the excess[above {limit_of_length}]. Length of `query_text` is {length}.')
                logger.warning('The translation result will be incomplete.')
                return query_text[:limit_of_length - 1]
        return query_text
