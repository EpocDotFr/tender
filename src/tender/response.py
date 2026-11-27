from tender.support import MimeType
from tender.gemtext import Gemtext
from typing import Optional
import asyncio


class Response:
    def __init__(
        self,
        status: int,
        body: Optional[bytes] = None,
        mime_type: Optional[MimeType] = None,
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
        try:
            status = (await reader.readuntil(b' '))[:-1]
        except asyncio.IncompleteReadError:
            raise ValueError('Incomplete status') from None

        try:
            if len(status) != 2:
                raise ValueError

            status = int(status.decode())
        except ValueError:
            raise ValueError(f'Malformed status: {status}') from None

        if Response.is_input(status):
            try:
                prompt = await reader.readuntil(b'\r\n')
            except asyncio.IncompleteReadError:
                raise ValueError('No prompt received') from None

            return Response(status, prompt=prompt[:-2].decode(errors='replace'))
        elif Response.is_success(status):
            try:
                mime_type = await reader.readuntil(b'\r\n')
            except asyncio.IncompleteReadError:
                mime_type = None

            mime_type = Response.parse_mime_type(mime_type[:-2] if mime_type else None)

            body = (await reader.read()) or b''
            gemtext = None

            if body and mime_type.media_type == 'text/gemini':
                try:
                    body_decoded = body.decode(mime_type.parameters.get('charset', 'utf-8'), errors='replace')
                except LookupError:
                    body_decoded = body.decode('utf-8', errors='replace')

                gemtext = Gemtext.create(
                    body_decoded,
                    mime_type.parameters.get('lang')
                )

            return Response(status, mime_type=mime_type, body=body, gemtext=gemtext)
        elif Response.is_redirect(status):
            try:
                uri = await reader.readuntil(b'\r\n')
            except asyncio.IncompleteReadError:
                raise ValueError('No uri received') from None

            return Response(status, uri=uri[:-2].decode(errors='replace'))
        elif Response.is_tempfail(status) or Response.is_permfail(status) or Response.is_auth(status):
            try:
                error_msg = await reader.readuntil(b'\r\n')
            except asyncio.IncompleteReadError as e:
                error_msg = e.partial

            return Response(
                status,
                error_msg=error_msg.removesuffix(b'\r\n').decode(errors='replace') if error_msg else None
            )
        else:
            raise ValueError(f'Invalid response status: {status}')

    def is_failure(self) -> bool:
        return Response.is_permfail(self.status) or Response.is_tempfail(self.status)

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

    @staticmethod
    def parse_mime_type(mime_type: Optional[bytes]) -> MimeType:
        if not mime_type:
            return MimeType('text/gemini', {'charset': 'utf-8'})

        mime_type = mime_type.lower().decode(errors='replace').replace(' ', '')

        if ';' in mime_type:
            mime_type, raw_params = mime_type.split(';', maxsplit=1)

            param_items = [
                raw_param.split('=', 1) for raw_param in raw_params.split(';') if '=' in raw_param
            ]

            params = {
                param[0]: param[1] for param in param_items
            }

            return MimeType(mime_type, params)
        else:
            return MimeType(mime_type, {})
