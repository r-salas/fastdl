#
#
#   Utils
#
#

import os.path
import mimetypes

from urllib.parse import urlparse


def splitext(path):
    """
    Split file into name and extension with support for .tar.gz / .tar.bz2 extensions

    Parameters
    -----------
    path: str
        File path

    Returns
    --------
    name: str
        File name
    extension: str
        File extension
    """
    for ext in [".tar.gz", ".tar.bz2"]:
        if path.endswith(ext):
            return path[:-len(ext)], path[-len(ext):]
    return os.path.splitext(path)


def lines(file_path, strip=True):
    """
    Read file line by line

    Parameters
    -----------
    file_path: str
        File path
    strip: bool
        Whether or not strip spaces from each line

    Yields
    ---------
    line: str
        Read line.
    """
    with open(file_path) as f:
        for line in f:
            if strip:
                line = line.strip()
            yield line


def guess_extension(content_type):
    """
    Guess extension

    Parameters
    -----------
    content_type: str
        MIME type

    Returns
    --------
    str
        Extension or None if not found
    """
    if content_type == "text/plain":
        ext = ".txt"
    else:
        ext = mimetypes.guess_extension(content_type)

    if ext == ".htm":
        ext = ".html"
    elif ext == ".jpe":
        ext = ".jpg"

    return ext


def filename_from_url(url):
    """
    Get filename from url

    Parameters
    ------------
    url: str
        Url to get filename

    Returns
    ---------
    str
        Filename
    """
    return os.path.basename(urlparse(url).path)
