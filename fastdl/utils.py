#
#
#   Utils
#
#

import os.path


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
