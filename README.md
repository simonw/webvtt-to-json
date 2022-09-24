# webvtt-to-json

[![PyPI](https://img.shields.io/pypi/v/webvtt-to-json.svg)](https://pypi.org/project/webvtt-to-json/)
[![Changelog](https://img.shields.io/github/v/release/simonw/webvtt-to-json?include_prereleases&label=changelog)](https://github.com/simonw/webvtt-to-json/releases)
[![Tests](https://github.com/simonw/webvtt-to-json/workflows/Test/badge.svg)](https://github.com/simonw/webvtt-to-json/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/webvtt-to-json/blob/master/LICENSE)

Convert WebVTT to JSON, optionally removing duplicate lines

## Installation

Install this tool using `pip`:

    pip install webvtt-to-json

## Usage

For help, run:

    webvtt-to-json --help

You can also use:

    python -m webvtt_to_json --help

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd webvtt-to-json
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
