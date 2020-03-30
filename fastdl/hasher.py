#
#
#   Hasher
#
#

import hashlib


def hash_file(fpath, algorithm="sha256", chunk_size=65535):
    """
    Calculates a file sha256 or md5 hash.

    Parameters
    ------------
        fpath: path to the file being validated
        algorithm: hash algorithm, one of "auto", "sha256", or "md5".
                The default "auto" detects the hash algorithm in use.
        chunk_size: Bytes to read at a time, important for large files.

    Examples
    -----------
    ```python
    >>> hash_file("/path/to/file.zip")
    e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    ```

    Returns
    ----------
        The file hash
    """
    hasher_map = {
        "sha256": hashlib.sha256,
        "sha512": hashlib.sha512,
        "sha1": hashlib.sha1,
        "md5": hashlib.md5
    }

    try:
        hasher = hasher_map[algorithm]()
    except KeyError:
        raise ValueError("Algorithm {} not supported. Available: {}".format(algorithm, list(hasher_map.keys())))

    with open(fpath, "rb") as fp:
        bytes_read = fp.read(chunk_size)
        while len(bytes_read) > 0:
            hasher.update(bytes_read)
            bytes_read = fp.read(chunk_size)

    return hasher.hexdigest()


def validate_file(fpath, file_hash, hash_algorithm="auto", chunk_size=65535):
    """
    Validate a file against a file hash.
    """
    if hash_algorithm == "auto":
        num_chars = len(file_hash)

        if num_chars == 64:
            hash_algorithm = "sha256"
        elif num_chars == 128:
            hash_algorithm = "sha512"
        elif num_chars == 40:
            hash_algorithm = "sha1"
        elif num_chars == 32:
            hash_algorithm = "md5"
        else:
            raise ValueError("`hash_algorithm='auto'` but we couldn't infer the hashing algorithm. "
                             "Please specify one.")

    return str(hash_file(fpath, hash_algorithm, chunk_size)) == str(file_hash)
