from typing import NamedTuple, Optional, List, Union


class Text(NamedTuple):
    text: str


class Link(NamedTuple):
    url: str
    label: Optional[str] = None


class Heading1(NamedTuple):
    text: str


class Heading2(NamedTuple):
    text: str


class Heading3(NamedTuple):
    text: str


class ListItem(NamedTuple):
    text: str


class Quote(NamedTuple):
    text: str


class Preformatted(NamedTuple):
    text: str
    alt: Optional[str] = None


class Gemtext:
    def __init__(self, lang: Optional[Union[str, List[str]]] = None):
        self.lines: List[Union[Text, Link, Heading1, Heading2, Heading3, ListItem, Quote, Preformatted]] = []
        self.lang = lang

    def append(self, line: Union[Text, Link, Heading1, Heading2, Heading3, ListItem, Quote, Preformatted]) -> Gemtext:
        self.lines.append(line)

        return self

    @staticmethod
    async def create(body: bytes, mime_type: str) -> Optional[Gemtext]:
        if not body:
            return None

        gemtext = Gemtext()

        return gemtext
