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
