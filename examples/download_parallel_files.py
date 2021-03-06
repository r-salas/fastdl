#
#
#   Parallel 2
#
#

import fastdl


URLS = [
    "https://file-examples.com/wp-content/uploads/2017/02/zip_9MB.zip",
    "https://file-examples.com/wp-content/uploads/2017/02/zip_10MB.zip",
    "https://file-examples.com/wp-content/uploads/2017/02/zip_5MB.zip"
]


with fastdl.Parallel(prefer="threads") as p:
    downloads = []

    for url in URLS:
        download = p.download(url, extract=True, dir_prefix="downloads", subdir_prefix="zip", content_disposition=True)
        downloads.append(download)

    file_paths = []

    for download in downloads:
        file_path = download.get()  # wait until is fully downloaded
        file_paths.append(file_path)

print(file_paths)
