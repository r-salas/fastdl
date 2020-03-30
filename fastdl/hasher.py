#
#
#   Hasher
#
#

import hashlib


def hash_file(fpath, algorithm="sha256", chunk_size=65535):
    """
    Calculates a file hash.

    Parameters
    ------------
    fpath: str
        Path to the file being validated
    algorithm: str
        Hash algorithm. One of the following: "sha256", "sha512", "sha1", "md5"
    chunk_size: int
        Bytes to read at a time

    Returns
    ----------
    file_hash: str
        The resulting file hash.

    Returns
    -------
    file_hash: str
        Resulting file hash
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

    Parameters
    ------------
    fpath: str
        Path to the file to validate
    file_hash: str
        File hash to validate
    hash_algorithm: str
        Hash algorithm to validate file. One of the following: "sha256", "sha512", "sha1", "md5"
        and "auto" (to infer algorithm). By default, it will try to infer algorithm according to length of file hash.

    Returns
    --------
    bool
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
