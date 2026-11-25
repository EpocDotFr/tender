from typing import NamedTuple, Optional, List, Union
import re

text_regex = re.compile(r'=>\s*(?P<url>\S+)(?:\s+(?P<label>.+))?')


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
            Heading1(text)
        )

    def heading_2(self, text: str) -> None:
        self.lines.append(
            Heading2(text)
        )

    def heading_3(self, text: str) -> None:
        self.lines.append(
            Heading3(text)
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
    def create(body: str, mime_type: str) -> Gemtext:
        lang = None

        mime_params = mime_type.replace(' ', '').removeprefix('text/gemini;').strip()

        if mime_params:
            lang_param = next((mime_param for mime_param in mime_params.split(';') if mime_param.startswith('lang=')), None)

            if lang_param:
                lang = lang_param.removeprefix('lang=').split(',')

        gemtext = Gemtext(lang)

        pre = False
        pre_text = ''
        pre_alt = None

        for line in body.splitlines():
            if line.startswith('```'):
                if not pre:
                    pre = True

                    pre_text = ''
                    pre_alt = line.removeprefix('```').lstrip() or None
                else:
                    pre = False

                    gemtext.preformatted(pre_text, pre_alt)
            elif pre:
                pre_text += f'{line}\r\n'
            elif line.startswith('=>'):
                match = text_regex.fullmatch(line)

                if match:
                    match = match.groupdict()

                    gemtext.link(match.get('url'), match.get('label')) # type: ignore[assignment]
                else:
                    gemtext.text(line)
            elif line.startswith('###'):
                gemtext.heading_3(
                    line.removeprefix('###').lstrip()
                )
            elif line.startswith('##'):
                gemtext.heading_2(
                    line.removeprefix('##').lstrip()
                )
            elif line.startswith('#'):
                gemtext.heading_1(
                    line.removeprefix('#').lstrip()
                )
            elif line.startswith('* '):
                gemtext.list_item(
                    line.removeprefix('*').lstrip()
                )
            elif line.startswith('>'):
                gemtext.quote(
                    line.removeprefix('>').lstrip()
                )
            else:
                gemtext.text(line)

        if pre:
            gemtext.preformatted(pre_text, pre_alt)

        return gemtext
