import click
import json
import webvtt


@click.command()
@click.version_option()
@click.argument("path", type=click.File("r"))
@click.option(
    "-o",
    "--output",
    type=click.File("w"),
    default="-",
    help="File to write output to",
)
def cli(path, output):
    "Convert WebVTT to JSON, optionally removing duplicate lines"
    captions = webvtt.read_buffer(path)
    out = [{"start": c.start, "end": c.end, "lines": c.lines} for c in captions]
    output.write(json.dumps(out, indent=2))
    output.write("\n")
    return
