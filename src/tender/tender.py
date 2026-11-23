from tender.response import Response
from urllib.parse import urlsplit

MAX_URI_LENGTH = 1024
SCHEME = 'gemini'


async def request(url: str) -> Response:
    # TODO Check length with MAX_URI_LENGTH

    try:
        url = urlsplit(url)
    except ValueError:
        raise ValueError('Invalid URI')

    if url.username or url.password:
        raise ValueError('URI with userinfo')
    elif url.fragment:
        raise ValueError('URI with fragment')
    elif url.scheme != SCHEME:
        raise ValueError(f'Invalid scheme: {url.scheme or "(none)"}')
