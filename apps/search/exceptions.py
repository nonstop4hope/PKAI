from rest_framework.exceptions import APIException


class CoreApiKeyFailed(Exception):
    pass


class TooManyRequests(APIException, Exception):
    status_code = 429
    default_detail = 'Too many requests. Please hold on'
    default_code = 'service_unavailable'


class RecordIsNotExists(APIException, Exception):
    status_code = 404
    default_detail = 'Sorry, can not find record'
    default_code = 'service_unavailable'


class CantDownloadFile(APIException, Exception):
    status_code = 400
    default_detail = 'Sorry, can not download file'
    default_code = 'service_unavailable'
