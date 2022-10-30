from rest_framework.exceptions import APIException


class CoreApiKeyFailed(Exception):
    pass


class TooManyRequests(APIException, Exception):
    status_code = 429
    default_detail = 'Too many requests. Please hold on'
    default_code = 'service_unavailable'
