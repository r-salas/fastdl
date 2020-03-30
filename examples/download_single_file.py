#
#
#   Download single file
#
#

from fastdl import download


URL = "https://file-examples.com/wp-content/uploads/2017/10/file-example_PDF_1MB.pdf"

file_path = download(URL, dir_prefix="downloads", force_download=True)

print(file_path)
