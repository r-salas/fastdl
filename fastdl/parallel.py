#
#
#   Parallel
#
#

from .downloader import download

from tqdm import tqdm
from multiprocessing import Pool, cpu_count
from multiprocessing.dummy import Pool as ThreadPool


class Parallel:
    """
    Parallel downloads done easily.

    Parameters
    -----------
    prefer: str
        One of the following: "threads" or "processes".
        For activities with high I/O such as a download to a file, it is recommended threads.
    max_workers: str
        Max workers to use. By default, the maximum workers will the number of available CPUs.

    Examples
    --------
    >>> with fastdl.Parallel(prefer="threads") as p:
            downloads = []

            for url in URLS:
                download = p.download(url, dir_prefix="downloads", extract=True)
                downloads.append(download)

            for download in downloads:
                file_path = download.get(timeout=5)  # wait until is fully downloaded
    """

    def __init__(self, prefer="threads", max_workers=None):
        if prefer == "threads":
            pool_cls = ThreadPool
        elif prefer == "processes":
            pool_cls = Pool
        else:
            raise ValueError("Expected argument to be `threads` or `processes` but got {}".format(prefer))

        if max_workers is None:
            max_workers = cpu_count()

        self.prefer = prefer
        self.max_workers = max_workers

        self._pool = pool_cls(max_workers, initializer=tqdm.set_lock, initargs=[tqdm.get_lock()])

    def download(self, *args, **kwargs):
        """
        Download file in parallel. The parameters will be the `fastdl.download()` parameters.

        Parameters
        ------------
        *args:
            Same as `fastdl.download()`
        **kwargs:
            Same as `fastdl.download()`

        Returns
        --------
        task: AsyncResult
            Parallel task. You should call `get()` method to wait until download is finished.
        """
        return self._pool.apply_async(download, args=args, kwds=kwargs)

    def close(self):
        self._pool.close()

    def __enter__(self):
        self._pool.__enter__()

        return self

    def __exit__(self, *args, **kwargs):
        self._pool.__exit__(*args, **kwargs)

    def __repr__(self):
        return "Parallel(prefer={}, max_workers={})".format(self.prefer, self.max_workers)
