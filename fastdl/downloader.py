#
#
#   Downloader
#
#

import os
import warnings

from .utils import splitext
from .parallel import parallel
from .hasher import validate_file
from .extractor import extract_file, can_extract

from tqdm import tqdm
from urllib.parse import urlparse
from urllib.request import urlopen
from urllib.error import ContentTooShortError


@parallel
def download(url, fname=None, dir_prefix=".", blocksize=1024 * 8, file_hash=None, hash_algorithm="auto",
             extract=False, extract_dir=None, progressbar=True):
    file_path = urlretrieve(url, fname=fname, dir_prefix=dir_prefix, blocksize=blocksize,
                            progressbar=progressbar, file_hash=file_hash, hash_algorithm=hash_algorithm)

    if not extract:
        return file_path

    if extract_dir is None:
        extract_dir, _ = splitext(file_path)

    if can_extract(file_path):
        return extract_file(file_path, extract_dir, progressbar=progressbar)
    else:
        warnings.warn("`extract=True` but {} can't be extracted".format(file_path))
        return file_path


@parallel
def urlretrieve(url, fname=None, dir_prefix=".", blocksize=1024 * 8, progressbar=True, reporthook=None, file_hash=None,
                hash_algorithm="auto"):
    """
    A more advance version of urllib.request.urlretrieve with support of progress bars, automatic file name,
    cache and file hash
    """
    with urlopen(url) as response:
        headers = response.info()

        if fname is None:
            fname = headers.get_filename()

        if fname is None:
            fname = os.path.basename(urlparse(url).path)

        if os.path.isabs(fname):
            file_path = fname
        else:
            os.makedirs(dir_prefix, exist_ok=True)
            file_path = os.path.join(dir_prefix, fname)

        if os.path.exists(file_path):
            if file_hash is not None and not validate_file(file_path, file_hash, hash_algorithm):
                warnings.warn("A local file was found, but it seems to be incomplete or outdated because the " +
                              hash_algorithm + " file hash does not match the original value of " + file_hash +
                              " so we will re-download the data.")
            else:
                return file_path

        content_length = int(headers.get("Content-Length", -1))

        blocknum = 0
        bytes_read = 0

        with open(file_path, "wb") as fp, tqdm(total=content_length, unit='B', unit_scale=True, miniters=1,
                                               unit_divisor=1024, desc="Downloading {}...".format(fname),
                                               disable=not progressbar) as pbar:
            while True:
                block = response.read(blocksize)
                if not block:
                    break

                fp.write(block)

                blocknum += 1
                bytes_read += len(block)

                if pbar is not None:
                    pbar.update(blocksize)

                if reporthook is not None:
                    reporthook(blocknum, blocksize, content_length)

    if content_length >= 0 and bytes_read < content_length:
        error_msg = "retrieval incomplete: got only {} out of {} bytes".format(bytes_read, content_length)
        raise ContentTooShortError(error_msg, (file_path, headers))

    return file_path
