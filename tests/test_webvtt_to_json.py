from click.testing import CliRunner
from webvtt_to_json.cli import cli
import json
import pathlib
import pytest

test_path = pathlib.Path(__file__).parent / "demo.vtt"


EXPECTED = [
    {
        "start": "00:00:00.000",
        "end": "00:00:01.829",
        "lines": [
            " ",
            "my<00:00:00.160><c> career</c><00:00:00.480><c> in</c><00:00:00.640><c> side</c><00:00:00.880><c> projects</c><00:00:01.280><c> and</c><00:00:01.520><c> open</c>",
        ],
    },
    {
        "start": "00:00:01.829",
        "end": "00:00:01.839",
        "lines": ["my career in side projects and open", " "],
    },
    {
        "start": "00:00:01.839",
        "end": "00:00:04.550",
        "lines": [
            "my career in side projects and open",
            "source<00:00:02.240><c> basically</c><00:00:02.800><c> this</c><00:00:03.040><c> is</c><00:00:03.199><c> so</c><00:00:03.360><c> i've</c><00:00:03.600><c> been</c>",
        ],
    },
    {
        "start": "00:00:04.550",
        "end": "00:00:04.560",
        "lines": ["source basically this is so i've been", " "],
    },
]


def test_webvtt_to_json():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, [str(test_path)])
        assert result.exit_code == 0
        assert json.loads(result.output) == EXPECTED


def test_webvtt_to_json_output():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, [str(test_path), "-o", "output.json"])
        assert result.exit_code == 0
        assert json.load(open("output.json")) == EXPECTED


@pytest.mark.parametrize("option", ("-d", "--dedupe"))
def test_webvtt_to_json_dedupe(option):
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, [str(test_path), option])
        assert result.exit_code == 0
        assert json.loads(result.output) == [
            {
                "start": "00:00:01.829",
                "end": "00:00:01.839",
                "lines": ["my career in side projects and open"],
            },
            {
                "start": "00:00:04.550",
                "end": "00:00:04.560",
                "lines": ["source basically this is so i've been"],
            },
        ]


@pytest.mark.parametrize("option", ("-s", "--single"))
def test_webvtt_to_json_dedupe_single(option):
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, [str(test_path), "-d", option])
        assert result.exit_code == 0
        assert json.loads(result.output) == [
            {
                "start": "00:00:01.829",
                "end": "00:00:01.839",
                "line": "my career in side projects and open",
            },
            {
                "start": "00:00:04.550",
                "end": "00:00:04.560",
                "line": "source basically this is so i've been",
            },
        ]

@pytest.mark.parametrize("option", ("-u", "--unify"))
def test_webvtt_to_json_dedup_unify_all_lines(option):
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, [str(test_path), "-d", option, 5000])
        assert result.exit_code == 0
        assert json.loads(result.output) == [
            {
                "start": "00:00:01.829",
                "end": "00:00:04.560",
                "lines": ["my career in side projects and open", "source basically this is so i've been"],
            }
        ]

@pytest.mark.parametrize("option", ("-u", "--unify"))
def test_webvtt_to_json_dedup_unify_no_lines(option):
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, [str(test_path), "-d", option, 10])
        assert result.exit_code == 0
        assert json.loads(result.output) == [
            {
                "start": "00:00:01.829",
                "end": "00:00:01.839",
                "lines": ["my career in side projects and open"],
            },
            {
                "start": "00:00:04.550",
                "end": "00:00:04.560",
                "lines": ["source basically this is so i've been"],
            },
        ]
