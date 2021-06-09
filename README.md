# fastdl
Download and extract files fast and easily.

```py
file_path = fastdl.download(url, extract=True, dir_prefix="downloads")
```

## Features

- Parallel downloads (threads and processes)
- Cache for downloads and extractions
- Easy extractions
- Progress bars
- Easily configurable

## Installation
```console
$ pip install fastdl
```

## Usage
`fastdl` can be be used in two different ways, download a single file or download multiple files in parallel:

**Single file**
```py
file_path = fastdl.download(url, dir_prefix="downloads", extract=True)
```

**Multiple files**
```py
with fastdl.Parallel(prefer="threads") as p:
    downloads = []

    for url in urls:
        download = p.download(url, dir_prefix="downloads") # same arguments
        downloads.append(download)

    for download in downloads:
        file_path = download.get()  # block until download is finished
```


### Parameters

| Parameter | Description | Type | Default |
| --- | --- | --- | --- |
| `url` | Url to download | str |  |
| `fname` | File name of download file. Can be an absolute path. Can receive a function with [response](https://docs.python.org/3/library/urllib.request.html#urllib.request.urlopen) as an argument | str or callable | `None` |
| `dir_prefix` | Directory to store download file. Used only if `fname` is not an absolute path. Defaults to current directory or value specified by `fastdl.conf["default_dir_prefix"]` | str | `None` |
| `subdir_prefix` | Subdirectory inside `dir_prefix` to store download. Defaults to no subdirectory. | str | `""` |
| `headers` | Dictionnary of HTTP headers to send. For example: `{"User-Agent": "fastdl/0.1"}` | dict | `{}` |
| `content_disposition` | Used only if `fname` is None. If `True`, try to infer the filename from content disposition. If `False`, url will be used to infer filename. | bool | `False` |
| `blocksize` | Number of bytes to read and write for each iteration | int | `8192` |
| `file_hash` | File hash. If the file hash doesn't match, it will be re-downloaded. | str | `None` |
| `hash_algorithm` | Hash algorithm. One of the following: `"sha256"`, `"sha512"`, `"sha1"`, `"md5"` or `auto`. By default, it will try to infer the algorithm according to the length of the `file_hash` | str | `auto` |
| `extract` | Whether or not extract file | bool | `False` |
| `extract_dir` | Directory to store extracted files. By default same directory as the file | str | `None` |
| `progressbar` | Whether or not show a progress bar | bool | `True` |
| `force_download` | Whether or not force download if file already exists. By default, it doesn't re-download file unless file hash doesn't match | bool | `False` |
| `force_extraction` | Whether or not force extraction if file already exists | bool | `False` |


## Examples

### Download file and re-download if hash doesn't match

```python
import fastdl

file_hash = "155fdb3732e82cc4864c441e6400def0"
url = "https://file-examples.com/wp-content/uploads/2017/02/zip_2MB.zip"

file_path = fastdl.download(url, extract=True, dir_prefix="downloads", file_hash=file_hash)
```

### Download multiple files in parallel

```python
import fastdl

urls = [
    "https://file-examples.com/wp-content/uploads/2017/04/file_example_MP4_480_1_5MG.mp4",
    "https://file-examples.com/wp-content/uploads/2017/04/file_example_MP4_640_3MG.mp4",
    "https://file-examples.com/wp-content/uploads/2017/04/file_example_MP4_1280_10MG.mp4"
]

with fastdl.Parallel(prefer="processes", max_workers=2) as p:
    downloads = []

    for url in urls:
        download = p.download(url, dir_prefix="downloads")

    for download in downloads:
        file_path = download.get(timeout=10)  # wait 10 seconds or raise timeout if download hasn't finished
```

### Download from a list of urls in parallel

```python
import fastdl
from fastdl.utils import lines

with fastdl.Parallel() as p:
    downloads = []

    for url in lines("urls.txt"):
        download = p.download(url)
        downloads.append(download)

    for download in downloads:
        file_path = download.get()
```

### Change default download directory

If you're using a directory for all your downloads (e.g ~/.myapp), you can easily change the default directory for your downloads:

```python
# myapp/__init__.py

import fastdl

fastdl.conf["default_dir_prefix"] = "~/.myapp"

# myapp/file.py

file_path = fastdl.download("https://file-examples.com/wp-content/uploads/2017/02/zip_2MB.zip")
file_path == "~/.myapp/zip_2MB.zip"
```
Check [examples](examples/) folder to see examples in action.
