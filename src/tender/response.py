from typing import Optional
import asyncio


class Response:
    def __init__(
        self,
        status: int,
        body: Optional[bytes] = None,
        mime_type: Optional[str] = None,
        prompt: Optional[str] = None,
        uri: Optional[str] = None,
        error_msg: Optional[str] = None
    ):
        self.status = status
        self.body = body
        self.mime_type = mime_type
        self.prompt = prompt
        self.uri = uri
        self.error_msg = error_msg

    @staticmethod
    async def create(reader: asyncio.StreamReader) -> Optional[Response]:
        status = await reader.readuntil(b' ')

        try:
            if len(status > 2):
                raise ValueError

            status = int(status[:-1].decode())
        except ValueError:
            raise ValueError(f'Malformed status: {status}')
        
        self.status = status

        if Response.is_input(status):
            self.prompt = (await reader.readuntil(b'\r\n'))[:-2].decode()
        if Response.is_success(status):
            self.mime_type = (await reader.readuntil(b'\r\n'))[:-2].decode()
            self.body = await reader.read()
        elif Response.is_redirect(status):
            self.uri = (await reader.readuntil(b'\r\n'))[:-2].decode()
        elif Response.is_tempfail(status) or Response.is_permfail(status) or Response.is_auth(status):
            error_msg = await reader.readuntil(b'\r\n')

            self.error_msg = error_msg[:-2].decode() if error_msg else None
        else:
            raise ValueError(f'Invalid status: {status}')

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
