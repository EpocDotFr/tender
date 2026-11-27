from tender.response import Response
from urllib.parse import urlsplit
import logging
import asyncio
import ssl

MAX_URL_LENGTH = 1024

logger = logging.getLogger('tender')


async def request(url: str, ssl_context: ssl.SSLContext, timeout: float | int = 5) -> Response:
    if len(url.encode()) > MAX_URL_LENGTH:
        raise ValueError(f'URL too long (must be max {MAX_URL_LENGTH} bytes)')

    try:
        parsed_url = urlsplit(url)
    except ValueError:
        raise ValueError('Invalid URL') from None

    if not parsed_url.hostname:
        raise ValueError('URL without hostname')
    if parsed_url.username or parsed_url.password:
        raise ValueError('URL with userinfo')
    elif parsed_url.fragment:
        raise ValueError('URL with fragment')
    elif parsed_url.scheme != 'gemini':
        raise ValueError(f'Invalid scheme: {parsed_url.scheme or "(none)"}')

    async with asyncio.timeout(timeout):
        reader, writer = await asyncio.open_connection(
            parsed_url.hostname,
            parsed_url.port or 1965,
            ssl=ssl_context,
            server_hostname=parsed_url.hostname
        )

        logger.debug(url)

        try:
            writer.write(f'{url}\r\n'.encode())

            await writer.drain()

            return await Response.create(reader)
        finally:
            writer.close()

            try:
                await writer.wait_closed()
            except Exception:
                pass
