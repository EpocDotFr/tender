from tender.response import Response
from urllib.parse import urlsplit


def request(url: str) -> Response:
    url = urlsplit(url)

    if url.username or url.password:
        raise ValueError('URI with userinfo')
    elif url.fragment:
        raise ValueError('URI with fragment')
    elif url.scheme != 'gemini':
        raise ValueError(f'Invalid scheme: {url.scheme or "(none)"}')
