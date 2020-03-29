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
