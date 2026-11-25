# Tender

A [Gemini](https://geminiprotocol.net/) (the protocol) low-level client, implemented in Python.

![Python versions](https://img.shields.io/pypi/pyversions/gemini-tender.svg) ![Version](https://img.shields.io/pypi/v/gemini-tender.svg) ![License](https://img.shields.io/pypi/l/gemini-tender.svg)

[PyPI](https://pypi.org/project/gemini-tender/) - [Documentation](https://github.com/EpocDotFr/tender?tab=readme-ov-file#usage) - [Source code](https://github.com/EpocDotFr/tender) - [Issue tracker](https://github.com/EpocDotFr/tender/issues) - [Changelog](https://github.com/EpocDotFr/tender/releases)

> [!TIP]
> See also: [Harbor](https://github.com/EpocDotFr/harbor), the accompanying server; and [Wayfarer](https://github.com/EpocDotFr/wayfarer), the accompanying [TUI](https://en.wikipedia.org/wiki/Text-based_user_interface) client.

## Prerequisites

  - Python >= 3.14

## Installation

Use your favorite Python package manager to install `gemini-tender`. Example using [Pipenv](https://pipenv.pypa.io/en/latest/):

```shell
pipenv install gemini-tender
```

## Usage

### Setting up the SSL context

The Gemini protocol *requires* usage of TLS >= 1.2. The first thing you thus have to do is to set up an SSL context.

A bare-minimum, Gemini-compliant context can be created and used right away:

```python
import tender

context = tender.create_default_ssl_context()
```

However, this context will *not* - by default - validate any certificate and will accept *any* certificate.

> [!NOTE]
> TODO

### Sending requests

As simple as (all examples assume you already have an asyncio context):

```python
import tender

context = ...

response = await tender.request('gemini://geminiprotocol.net/', context)
```

A `tender.Response` instance will be returned.

### Inspecting the response

Several attributes and methods in `tender.Response` are available:

  - `is_failure()` determines whether the status is a permanent or temporary failure
  - `is_input()`, `is_success()`, `is_redirect()`, `is_tempfail()`, `is_permfail()` and `is_auth()` determine the status group
  - `status` is the status as an integer
  - For input responses:
    - `prompt` is the prompt as a string
  - For success responses:
    - `body` is the raw response body as bytes
    - `mime_type` is a `tender.MimeType` instance (read below for more info)
    - `gemtext` may be a `tender.Gemtext` instance if the returned MIME type is `text/gemini`, or `None` instead. Read below for more info
  - For redirect responses:
    - `uri` is the redirect URI as a string
  - For temporary failure, permanent failure and auth responses:
    - `error_msg` is the error message as a string or `None` if there is none

#### Inspecting the response's MIME type

`tender.MimeType` is a named tuple, with the following attributes:

  - `media_type` - a string containing the actual MIME type (e.g. `text/gemini`)
  - `parameters` - a dictionary containing the associated parameters (e.g. `{'charset': 'utf-8', 'lang': 'fr'}`)

#### Reading the parsed gemtext

`tender.Gemtext` exposes the following attributes:

  - `lines` - a list of parsed lines constituting the gemtext document. This list may contain instances of the following named tuples and associated attributes:
    - `tender.Text` (`text` - string)
    - `tender.Link` (`url` - string, `label` - string or `None`)
    - `tender.Heading1` (`text` - string)
    - `tender.Heading2` (`text` - string)
    - `tender.Heading3` (`text` - string)
    - `tender.ListItem` (`text` - string)
    - `tender.Quote` (`text` - string)
    - `tender.Preformatted` (`text` - string, `alt` - string or `None`)
  - `lang` - a list of language codes, parsed from the response's MIME type, or `None` if there's none

## Development

### Getting source code and installing the package

  1. Clone the repository
  2. Run for example: `pipenv install --editable path/to/the/package-root-dir`

### Releasing the package

> [!NOTE]
> TODO

`__version__` in `src/tender/__init__.py` must be updated beforehand. It should adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

An associated GitHub release must be created following the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
format.