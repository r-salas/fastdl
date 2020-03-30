#
#
#   Downloader
#
#

import os
import warnings

from .config import conf

from .utils import splitext
from .hasher import validate_file
from .extractor import extract_file, can_extract

from tqdm import tqdm
from urllib.parse import urlparse
from urllib.request import urlopen, Request
from urllib.error import ContentTooShortError


def download(url, fname=None, dir_prefix=".", headers=None, blocksize=1024 * 8, file_hash=None, hash_algorithm="auto",
             extract=False, extract_dir=None, progressbar=True, force_download=False, force_extraction=False):
    """
    Download files with support for extractions and hash validations.

    Parameters
    ------------
    url: str
        Url to download
    fname: str, optional
        File name for the download file. If not provided, it will try to infer filename using
        info from the server or the url. Can be an absolute path.
    dir_prefix: str
        Directory to download files (if `fname` is not an absolute path). By default, it will
        download files to current working directory.
    headers: dict, optional
        Dictionnary of headers to send during request.
    blocksize: int
        Response blocks to read / write for every iteration
    file_hash: str, optional
        File hash to validate file. If hash doesn't match, it will re-download file.
    hash_algorithm: str
        Hash algorithm to validate file. Currently supported: "sha256", "sha1", "sha512", "md5".
        By default, it will try to infer algorithm according to the number of characters of the file
        hash.
    extract: str
        Whether or not the file should be extracted. The currently supported extensions are the
        following: "zip", "tar", "tar.gz", "tar.bz2"
    extract_dir: str
        Directory to extract files. By default, the directory will be the same as the download file.
    progressbar: str
        Whether or not show progress bar.
    force_download: bool
        Whether or not force download if file already exists.
    force_extraction: bool
        Whether or not force extraction if file already exists.

    Returns
    --------
    file_path: str
        Download file path
    """
    if dir_prefix is None:
        dir_prefix = conf["default_dir_prefix"]
                             progressbar=progressbar, file_hash=file_hash, hash_algorithm=hash_algorithm,
                             force_download=False)

    if not extract:
        return file_path

    if extract_dir is None:
        extract_dir, _ = splitext(file_path)

    if not can_extract(file_path):
        warnings.warn("`extract=True` but {} can't be extracted".format(file_path))
        return file_path

    extract_file(file_path, extract_dir, force=force_extraction, progressbar=progressbar)

    return file_path


def _urlretrieve(url, fname=None, dir_prefix=".", headers=None, blocksize=1024 * 8, progressbar=True, reporthook=None,
                 file_hash=None, hash_algorithm="auto", force_download=False):
    """
    A more advance version of urllib.request.urlretrieve with support of progress bars,
    automatic file name, cache and file hash
    """
    if headers is None:
        headers = {}

    request = Request(url, headers=headers)

    with urlopen(request) as response:
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

        if os.path.exists(file_path) and not force_download:
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
