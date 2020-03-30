#
#
#   Download from file of urls
#
#

from pathlib import Path

from fastdl import Parallel
from fastdl.utils import lines

FILE_PATH = Path(__file__).parent / "urls.txt"

with Parallel(prefer="threads") as p:
    downloads = []

    for url in lines(FILE_PATH):
        download = p.download(url, dir_prefix="downloads", headers={"User-Agent": "fastdl"})
        downloads.append(download)

    file_paths = []

    for download in downloads:
        file_path = download.get()
        file_paths.append(file_path)

print(file_paths)
