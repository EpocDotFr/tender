from tender.response import Response
from urllib.parse import urlsplit
from typing import Optional
import logging
import asyncio

MAX_URI_LENGTH = 1024

logger = logging.getLogger('tender')


async def request(url: str) -> Optional[Response]:
    # TODO Check length with MAX_URI_LENGTH

    try:
        url = urlsplit(url)
    except ValueError:
        raise ValueError('Invalid URI')

    if url.username or url.password:
        raise ValueError('URI with userinfo')
    elif url.fragment:
        raise ValueError('URI with fragment')
    elif url.scheme != 'gemini':
        raise ValueError(f'Invalid scheme: {url.scheme or "(none)"}')

    reader, writer = await asyncio.open_connection(url.hostname, url.port or 1965)

    logger.debug(url)

    try:
        writer.write(f'{url}\r\n'.encode())

        await writer.drain()
    except (BrokenPipeError, ConnectionResetError):
        pass
    except Exception:
        logger.exception('Error writing request')

    try:
        return await Response.create(reader)
    except (BrokenPipeError, ConnectionResetError):
        pass
    except Exception:
        logger.exception('Error reading response')
    finally:
        writer.close()

        try:
            await writer.wait_closed()
        except Exception:
            pass

    return None
