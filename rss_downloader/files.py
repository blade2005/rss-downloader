"""File related functions for RSS Downloader."""
import argparse
import pathlib
from typing import Generator, List, Tuple

import feedparser


def _output_path(output_dir: str, title: str, href: str) -> pathlib.PurePath:
    """Join path from the base dir, title, and href."""
    return pathlib.PurePath(output_dir, title + pathlib.PurePath(href).suffix)


def files_generator(
    entries: List[feedparser.util.FeedParserDict], args: argparse.Namespace
) -> Generator[Tuple[pathlib.PurePath, str, str], None, None]:
    """Generate entries to download."""
    # import code;code.interact(local={**globals(),**locals()})
    for entry in entries:
        entry.title
        for link in entry.links:
            if link.type.startswith("audio"):
                yield (
                    _output_path(args.output_dir, entry.title, link.href),
                    entry.title,
                    link.href,
                )
        # break
