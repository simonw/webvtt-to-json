import click
import json
import webvtt


@click.command()
@click.version_option()
@click.argument("path", type=click.File("r"))
@click.option("-d", "--dedupe", is_flag=True, help="Remove duplicate lines")
@click.option("-s", "--single", is_flag=True, help='Output single "line": per item')
@click.option(
    "-o",
    "--output",
    type=click.File("w"),
    default="-",
    help="File to write output to",
)
def cli(path, dedupe, single, output):
    "Convert WebVTT to JSON, optionally removing duplicate lines"
    captions = webvtt.read_buffer(path)
    dicts = [{"start": c.start, "end": c.end, "lines": c.lines} for c in captions]
    if dedupe:
        dicts = []
        prev_line = None
        for c in captions:
            if any("<c>" in l for l in c.lines):
                continue
            # Collect lines that are not dupes
            not_dupe_lines = []
            for line in c.lines:
                if not line.strip():
                    continue
                if line != prev_line:
                    not_dupe_lines.append(line)
                prev_line = line
            if not_dupe_lines:
                dicts.append({"start": c.start, "end": c.end, "lines": not_dupe_lines})
    if single:
        for d in dicts:
            d["line"] = "\n".join(d.pop("lines"))
    output.write(json.dumps(dicts, indent=2))
    output.write("\n")
    return
