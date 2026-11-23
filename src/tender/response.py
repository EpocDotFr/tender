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
        # TODO Parse and validate response
        pass

    def is_input(self) -> bool:
        return 10 <= self.status <= 19

    def is_success(self) -> bool:
        return 20 <= self.status <= 29

    def is_redirect(self) -> bool:
        return 30 <= self.status <= 39

    def is_tempfail(self) -> bool:
        return 40 <= self.status <= 49

    def is_permfail(self) -> bool:
        return 50 <= self.status <= 59

    def is_auth(self) -> bool:
        return 60 <= self.status <= 69
