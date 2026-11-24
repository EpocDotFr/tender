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

    def text(self, text: str) -> None:
        self.lines.append(
            Text(text)
        )

    def link(self, url: str, label: Optional[str] = None) -> None:
        self.lines.append(
            Link(url, label)
        )

    def heading_1(self, text: str) -> None:
        self.lines.append(
            Heading1(label)
        )

    def heading_2(self, text: str) -> None:
        self.lines.append(
            Heading2(label)
        )

    def heading_3(self, text: str) -> None:
        self.lines.append(
            Heading3(label)
        )

    def list_item(self, text: str) -> None:
        self.lines.append(
            ListItem(text)
        )

    def quote(self, text: str) -> None:
        self.lines.append(
            Quote(text)
        )

    def preformatted(self, text: str, alt: Optional[str] = None) -> None:
        self.lines.append(
            Preformatted(text, alt)
        )

    @staticmethod
    def create(body: str, mime_type: str) -> Optional[Gemtext]:
        lang = None

        raw_lang = mime_type.replace(' ', '').removeprefix('text/gemini;').strip()

        if raw_lang.startswith('lang='):
            lang = raw_lang.removeprefix('lang=').split(',')

        gemtext = Gemtext(lang)

        pre = False
        pre_text = ''
        pre_alt = None

        for line in body.splitlines():
            if line.startswith('=>'):
                pass # TODO
            elif line.startswith('###'):
                pass # TODO
            elif line.startswith('##'):
                pass # TODO
            elif line.startswith('#'):
                pass # TODO
            elif line.startswith('* '):
                pass # TODO
            elif line.startswith('> '):
                pass # TODO
            elif line.startswith('```'):
                if not pre:
                    pre = True

                    pre_text = ''
                    pre_alt = line.removesuffix('```').strip() or None
                else:
                    pre = False

                    gemtext.preformatted(pre_text, pre_alt)
            elif pre:
                pre_text += f'{line}\r\n'
            else:
                gemtext.text(line)

        return gemtext
