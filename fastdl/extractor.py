#
#
#   Extractor
#
#

import zipfile
import tarfile

from tqdm import tqdm


def can_extract(file_path):
    return _to_extractor(file_path) is not None


def extract_file(file_path, extract_dir=".", progressbar=True, ):
    """
    Unpack `file_path` to `extract_dir`.
    """
    extractor = _to_extractor(file_path)

    if extractor is None:
        raise ValueError("File {} not supported for extraction".format(file_path))

    return extractor(file_path, extract_dir, progressbar)


def _extract_zip(file_path, extract_dir=".", progressbar=True):
    """
    Unpack zip `filename` to `extract_dir`
    """
    with zipfile.ZipFile(file=file_path) as zip_file:
        iterator = zip_file.namelist()

        if progressbar:
            iterator = tqdm(iterator, total=len(iterator), unit="", desc="Extracting files...")

        for file in iterator:
            zip_file.extract(member=file, path=extract_dir)

    return extract_dir


def _extract_tar(file_path, extract_dir=".", progressbar=True):
    """
    Unpack tar/tar.gz/tar.bz2
    """
    with tarfile.open(file_path) as tarball:
        iterator = tarball.getmembers()

        if progressbar:
            iterator = tqdm(iterator, total=len(iterator), unit="", desc="Extracting files...")

        for member in iterator:
            tarball.extract(member=member, path=extract_dir)

    return extract_dir


def _to_extractor(file_path):
    if zipfile.is_zipfile(file_path):
        return _extract_zip
    elif tarfile.is_tarfile(file_path):
        return _extract_tar

    return None
