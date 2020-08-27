#
#
#   Extractor
#
#

import zipfile
import tarfile

from tqdm.auto import tqdm
from os.path import isfile, join


def can_extract(file_path):
    """
    Whether or not fastdl can extract this file.

    Parameters
    -----------
    file_path: str
        File path to check.

    Returns
    --------
    bool
    """
    return _to_extractor(file_path) is not None


def extract_file(file_path, extract_dir=".", progressbar=True, force=False):
    """
    Extract file to directory.

    Parameters
    ------------
    file_path: str
        File path to extract
    extract_dir: str
        Extraction directory
    progressbar: bool
        Whether or not show progressbar.
    force: bool
        Whether or not force extraction if file already exists
    """
    extractor = _to_extractor(file_path)

    if extractor is None:
        raise ValueError("File {} not supported for extraction".format(file_path))

    return extractor(file_path, extract_dir, progressbar=progressbar, force=force)


def _extract_zip(file_path, extract_dir=".", progressbar=True, force=False):
    """
    Unpack zip `filename` to `extract_dir`
    """
    with zipfile.ZipFile(file=file_path) as zip_file:
        iterator = zip_file.namelist()

        if progressbar:
            iterator = tqdm(iterator, total=len(iterator), unit="", desc="Extracting files...")

        for member in iterator:
            if not isfile(join(extract_dir, member)) or force:
                zip_file.extract(member=member, path=extract_dir)

    return extract_dir


def _extract_tar(file_path, extract_dir=".", progressbar=True, force=False):
    """
    Unpack tar/tar.gz/tar.bz2
    """
    with tarfile.open(file_path) as tarball:
        iterator = tarball.getmembers()

        if progressbar:
            iterator = tqdm(iterator, total=len(iterator), unit="", desc="Extracting files...")

        for member in iterator:
            if not isfile(join(extract_dir, member.name)) or force:
                tarball.extract(member=member, path=extract_dir)

    return extract_dir


def _to_extractor(file_path):
    if zipfile.is_zipfile(file_path):
        return _extract_zip
    elif tarfile.is_tarfile(file_path):
        return _extract_tar
