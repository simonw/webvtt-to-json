import click
import json
import webvtt

from datetime import datetime


def time_diff_in_milliseconds(start, end):
    start_dt = datetime.strptime(start, "%H:%M:%S.%f")
    end_dt = datetime.strptime(end, "%H:%M:%S.%f")
    diff = (end_dt - start_dt).total_seconds() * 1000
    return diff

@click.command()
@click.version_option()
@click.argument("path", type=click.File("r"))
@click.option("-d", "--dedupe", is_flag=True, help="Remove duplicate lines")
@click.option("-s", "--single", is_flag=True, help='Output single "line": per item')
@click.option("-u", "--unify", type=int, default=-1, help='Unify lines with less than "unify" milliseconds pause between them')
@click.option(
    "-o",
    "--output",
    type=click.File("w"),
    default="-",
    help="File to write output to",
)
def cli(path, dedupe, single, unify, output):
    "Convert WebVTT to JSON, optionally removing duplicate lines and unifying lines with a short pause in between"
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
    if unify >= 0:
        new_dicts = []
        prev_dict = None
        for d in dicts:
            if prev_dict is None:
                prev_dict = d
                continue
            # Unify lines with a short pause between them
            if time_diff_in_milliseconds(prev_dict["end"], d["start"]) < unify:
                prev_dict["end"] = d["end"]
                for line in d["lines"]:
                    if line not in prev_dict["lines"]:
                        prev_dict["lines"] += [line, ]
            else:
                new_dicts.append(prev_dict)
                prev_dict = {"start": c.start, "end": c.end, "lines": d["lines"]}
        if prev_dict is not None:
            new_dicts.append(prev_dict)
        dicts = new_dicts
    if single:
        for d in dicts:
            d["line"] = "\n".join(d.pop("lines"))

    output.write(json.dumps(dicts, indent=2))
    output.write("\n")
    return
