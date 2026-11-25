from typing import NamedTuple, Dict
import ssl


def create_default_ssl_context() -> ssl.SSLContext:
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
    ssl_context.load_default_certs(ssl.Purpose.SERVER_AUTH)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    return ssl_context


class MimeType(NamedTuple):
    media_type: str
    parameters: Dict[str, str]
