from tender.gemtext import Gemtext
from typing import Optional
import asyncio


class Response:
    def __init__(
        self,
        status: int,
        body: Optional[bytes] = None,
        mime_type: Optional[str] = None,
        gemtext: Optional[Gemtext] = None,
        prompt: Optional[str] = None,
        uri: Optional[str] = None,
        error_msg: Optional[str] = None
    ):
        self.status = status
        self.body = body
        self.mime_type = mime_type
        self.gemtext = gemtext
        self.prompt = prompt
        self.uri = uri
        self.error_msg = error_msg

    @staticmethod
    async def create(reader: asyncio.StreamReader) -> Response:
        status = (await reader.readuntil(b' '))[:-1]

        try:
            if len(status) > 2:
                raise ValueError

            status = int(status.decode())
        except ValueError:
            raise ValueError(f'Malformed status: {status}') from None

        if Response.is_input(status):
            prompt = await reader.readuntil(b'\r\n')

            if not prompt:
                raise ValueError('No prompt received')

            return Response(status, prompt=prompt[:-2].decode())
        if Response.is_success(status):
            mime_type = await reader.readuntil(b'\r\n')

            if not mime_type:
                raise ValueError('No mime type received')
            
            mime_type = mime_type[:-2].decode()

            body = (await reader.read()) or b''
            gemtext = Gemtext.create(body, mime_type) if mime_type.startswith('text/gemini') else None

            return Response(status, mime_type=mime_type, body=body, gemtext=gemtext)
        elif Response.is_redirect(status):
            uri = await reader.readuntil(b'\r\n')

            if not uri:
                raise ValueError('No uri received')

            return Response(status, uri=uri[:-2].decode())
        elif Response.is_tempfail(status) or Response.is_permfail(status) or Response.is_auth(status):
            error_msg = await reader.readuntil(b'\r\n')

            return Response(status, error_msg=error_msg[:-2].decode() if error_msg else None)
        else:
            raise ValueError(f'Invalid response status: {status}')

    @staticmethod
    def is_input(status: int) -> bool:
        return 10 <= status <= 19

    @staticmethod
    def is_success(status: int) -> bool:
        return 20 <= status <= 29

    @staticmethod
    def is_redirect(status: int) -> bool:
        return 30 <= status <= 39

    @staticmethod
    def is_tempfail(status: int) -> bool:
        return 40 <= status <= 49

    @staticmethod
    def is_permfail(status: int) -> bool:
        return 50 <= status <= 59

    @staticmethod
    def is_auth(status: int) -> bool:
        return 60 <= status <= 69
