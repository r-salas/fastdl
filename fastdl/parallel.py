#
#
#   Parallel
#
#

from tqdm import tqdm
from multiprocessing import Pool, cpu_count
from multiprocessing.dummy import Pool as ThreadPool


class Blueprint:
    """
    A blueprint with the ingredientes to call a function.
    """

    def __init__(self, target, args=None, kwargs=None):
        if args is None:
            args = []

        if kwargs is None:
            kwargs = {}

        self.target = target
        self.args = args
        self.kwargs = kwargs

    def __repr__(self):
        return "Blueprint(target={}, args={}, kwargs={})".format(self.target, self.args, self.kwargs)


def parallel(func):
    """
    Convert a function into a blueprinter.
    """
    def blueprinter(*args, **kwargs):
        return Blueprint(target=func, args=args, kwargs=kwargs)

    func.parallel = blueprinter
    return func


def get(blueprints, prefer="threads", max_workers=None, timeout=None):
    """
    Start parallel processes

    Parameters
    -----------
    blueprints: list of Blueprint
        A collection of blueprints (returned value by calling `func.parallel`)
    prefer: str
        Use `threads` or `processes`
    max_workers: int, optional
        Maximum workers
    timeout: int, optional
        Maximum time in seconds to wait for results

    Returns
    --------
    list of values
        List of returned values
    """
    if prefer == "threads":
        pool_cls = ThreadPool
    elif prefer == "processes":
        pool_cls = Pool
    else:
        raise ValueError("Expected argument to be `threads` or `processes` but got {}".format(prefer))

    if max_workers is None:
        max_workers = cpu_count()

    processes = min(len(blueprints), max_workers)

    with pool_cls(processes, initializer=tqdm.set_lock, initargs=[tqdm.get_lock()]) as pool:

        tasks = []
        for blueprint in blueprints:
            task = pool.apply_async(blueprint.target, args=blueprint.args, kwds=blueprint.kwargs)
            tasks.append(task)

        results = []
        for task in tasks:
            result = task.get(timeout=timeout)
            results.append(result)

    return results
