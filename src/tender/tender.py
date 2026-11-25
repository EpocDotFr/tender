from tender.response import Response
from urllib.parse import urlsplit
import logging
import asyncio
import ssl

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
ssl_context.load_default_certs(ssl.Purpose.SERVER_AUTH)
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

MAX_URI_LENGTH = 1024

logger = logging.getLogger('tender')


async def request(url: str, timeout: float | int = 5) -> Response:
    # TODO Check length with MAX_URI_LENGTH

    try:
        parsed_url = urlsplit(url)
    except ValueError:
        raise ValueError('Invalid URI') from None

    if parsed_url.username or parsed_url.password:
        raise ValueError('URI with userinfo')
    elif parsed_url.fragment:
        raise ValueError('URI with fragment')
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
