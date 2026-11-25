# Tender

A [Gemini](https://geminiprotocol.net/) (the protocol) low-level client, implemented in Python.

![Python versions](https://img.shields.io/pypi/pyversions/gemini-tender.svg) ![Version](https://img.shields.io/pypi/v/gemini-tender.svg) ![License](https://img.shields.io/pypi/l/gemini-tender.svg)

[PyPI](https://pypi.org/project/tender/) - [Documentation](https://github.com/EpocDotFr/tender?tab=readme-ov-file#usage) - [Source code](https://github.com/EpocDotFr/tender) - [Issue tracker](https://github.com/EpocDotFr/tender/issues) - [Changelog](https://github.com/EpocDotFr/tender/releases)

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

> [!NOTE]
> TODO

## Development

### Getting source code and installing the package

  1. Clone the repository
  2. From the root directory, run for example: `pipenv install --editable path/to/the/package-root-dir"`

### Releasing the package

> [!NOTE]
> TODO

`__version__` in `src/tender/__init__.py` must be updated beforehand. It should adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

An associated GitHub release must be created following the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
format.