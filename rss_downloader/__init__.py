"""Blank file for Python transversal.

This can be deleted or renamed to store the source code of your project.

"""
import argparse
import logging
import pathlib
from multiprocessing.dummy import Pool
from typing import Tuple

import feedparser

from rss_downloader.downloads import download_file
from rss_downloader.files import files_generator

FORMAT = "%(asctime)-15s %(levelname)s %(module)s.%(funcName)s %(message)s"
DATEFMT = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt=DATEFMT)


def parse_args() -> argparse.Namespace:
    """Parse CLI Args."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r",
        "--rss-feed",
        type=str,
        action="store",
        required=True,
        help="URL of RSS Feed",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        action="store",
        required=True,
        help="Output Directory",
    )
    return parser.parse_args()


def _map_download_file(args: Tuple[pathlib.PurePath, str, str]) -> bool:
    """Execute download_file from Pool.map."""
    return download_file(*args)


def main():
    """Run CLI Script."""
    args = parse_args()
    feed = feedparser.parse(args.rss_feed)
    pathlib.Path(args.output_dir).mkdir(exist_ok=True)
    pool = Pool(10)
    queue = list(files_generator(feed.entries, args))
    logging.info("Files in queue: %s", len(queue))
    pool.map(_map_download_file, queue)
    pool.close()
    pool.join()
