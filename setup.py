from setuptools import setup
import os

VERSION = "0.2"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="webvtt-to-json",
    description="Convert WebVTT to JSON, optionally removing duplicate lines",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/webvtt-to-json",
    project_urls={
        "Issues": "https://github.com/simonw/webvtt-to-json/issues",
        "CI": "https://github.com/simonw/webvtt-to-json/actions",
        "Changelog": "https://github.com/simonw/webvtt-to-json/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["webvtt_to_json"],
    entry_points="""
        [console_scripts]
        webvtt-to-json=webvtt_to_json.cli:cli
    """,
    install_requires=["click", "webvtt-py"],
    extras_require={"test": ["pytest"]},
    python_requires=">=3.7",
)
