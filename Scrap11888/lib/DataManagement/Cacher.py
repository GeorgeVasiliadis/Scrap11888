import os
import pickle

from .Utils import purify

def cacheIn(dir, name, data):
    """
    Store given `data` under ./cache/dir/name.pickle file.
    Note that `dir` and `name` are "purified" before used!

    -dir: string of sub-directory to be created. Cache-file will be stored in it.
        It shouldn't be None.
    -name: string of filename without any extension. Cache-file will be named
        after it. It shouldn't be None.
    -data: python object to be cached.
    """

    path = "cache"
    dir = purify(dir)
    name = purify(name)
    path = os.path.join(path, dir)

    # If specified file exists, overwrite it without errors or warnings.
    os.makedirs(path, exist_ok=True)

    filename = name + ".pickle"
    path = os.path.join(path, filename)

    with open(path, "wb") as file:
        pickle.dump(data, file)

def cacheOut(dir, name):
    """
    Try to retrieve cached data under `./cache/dir/name.pickle`. If the
    cache-file doesn't exist, None is being returned.
    Note that `dir` and `name` are "purified" before used!

    -dir: string of sub-directory to searched for cache-file. It shouldn't be
        None.
    -name: string of filename to be searched without any extension. It shouldn't
    be None.
    """

    data = None

    path = "cache"
    dir = purify(dir)
    name = purify(name)
    filename = name + ".pickle"
    path = os.path.join(path, dir, filename)

    if os.path.isfile(path):
        with open(path, "rb") as file:
            data = pickle.load(file)

    return data
