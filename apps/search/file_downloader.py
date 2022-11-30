import os
import urllib
from urllib.parse import urlparse

import magic
import wget
from django.conf import settings

from apps.search.exceptions import CantDownloadFile
from apps.search.models import DownloadedFile


def get_file_from_url(url: str) -> DownloadedFile:
    if not os.path.exists(settings.TEMP_DIR):
        os.makedirs(settings.TEMP_DIR)
    try:
        filename = os.path.basename(urlparse(url).path)
        file_path = os.path.join(settings.TEMP_DIR, filename)
        wget.download(url, file_path)
        mime = magic.Magic(mime=True)
        return DownloadedFile(name=filename, path=file_path, content_type=mime.from_file(file_path))
    except (ValueError, urllib.error.HTTPError, urllib.error.URLError):
        raise CantDownloadFile
