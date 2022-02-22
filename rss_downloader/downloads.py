"""Download related imports for RSS Downloader."""
import logging
import os
import pathlib

import requests


def _write_file(
    response: requests.models.Response, output_path: pathlib.PurePath
) -> None:
    """Write file from requests.response to disk."""
    with open(output_path, "wb") as outfile:
        if response.status_code == 200:
            # import code; code.interact(local={**globals(), **locals()})
            bytes_written = 0
            for chunk in response.iter_content(1024):
                bytes_written += outfile.write(chunk)
            logging.debug("Wrote %s bytes for %s", bytes_written, output_path)


def _clean_up_empty_files(output_path: pathlib.PurePath) -> bool:
    """If the file is empty, remove it."""
    if is_empty(output_path):
        logging.warn("File %s is empty; Removing.", output_path)
        pathlib.Path(output_path).unlink()
        return False
    return True


def download_file(output_path: pathlib.PurePath, title: str, href: str) -> bool:
    """Download file to path."""
    if pathlib.Path(output_path).exists():
        logging.warn("Skipping %s", title)
        return False
    logging.info("Downloading %s", title)

    _write_file(requests.get(href, stream=True), output_path)
    # import code; code.interact(local={**globals(), **locals()})
    return _clean_up_empty_files(output_path)


def is_empty(path: pathlib.PurePath) -> bool:
    """Check if path is an empty file."""
    try:
        return not os.path.getsize(path) > 0
    except OSError:
        return True
