import os
import errno
from shutil import rmtree
from pprint import pformat


## Filesystem utilities
def mkdir_p(path):
    """Like `mkdir -p` in unix"""
    if not path.strip():
        return
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def rm_f(path):
    """Like `rm -f` in unix"""
    try:
        os.unlink(path)
    except OSError as e:
        if e.errno == errno.ENOENT:
            pass
        else:
            raise


def rm_rf(path):
    """Like `rm -rf` in unix"""
    return rmtree(path, ignore_errors=True)


def update_file(path, data):
    """Writes data to path, creating path if it doesn't exist"""
    # delete file if already exists
    rm_f(path)

    # create parent dirs if needed
    parent_dir = os.path.dirname(path)
    if not os.path.isdir(os.path.dirname(parent_dir)):
        mkdir_p(parent_dir)

    # write file
    with open(path, 'w') as f:
        f.write(data)


def put_data(data, path):
    """Creates parent dirs if needed, then writes data to path"""
    dir = os.path.dirname(path)
    mkdir_p(dir)
    update_file(path, data)


def list_subdirs(path):
    subfiles = [os.path.join(path, fn) for fn in os.listdir(path)]
    subdirs = [dir for dir in subfiles if os.path.isdir(dir)]
    return subdirs


def search_dirs(path, condition):
    rv = []
    if condition(path):
        rv.append(path)

    if not os.path.isdir(path):
        return rv

    stack = [path]

    while stack:
        cur = stack.pop()
        subfiles = [os.path.join(cur, fn) for fn in os.listdir(cur)]
        rv.extend(fpath for fpath in subfiles if condition(fpath))
        stack.extend(list_subdirs(cur))
    return rv


def locate(dirpath, condition):
    """Same as search_dirs, but make sure there is only one result"""
    dirpaths = search_dirs(dirpath, condition)

    # Make sure there is exactly one such dir
    if not dirpaths:
        raise Exception("No such item found!")
    elif len(dirpaths) > 1:
        raise Exception("Multiple found! They are:\n %s" % pformat(dirpaths))
    return dirpaths[0]


def locate_shallowest(dirpath, condition):
    """Same as search_dirs, but make sure there is only one shallowest result"""
    dirpaths = search_dirs(dirpath, condition)

    # Make sure there is exactly one such dir
    if not dirpaths:
        raise Exception("No such item found!")
    elif len(dirpaths) > 1:
        def path_depth(p):
            elts = p.split(os.path.sep)
            return len(elts)

        shallowest_depth = min(path_depth(fn) for fn in dirpaths)
        dirpaths = [path for path in dirpaths if path_depth(path) == shallowest_depth]
        if len(dirpaths) > 1:
            raise Exception("Multiple found! They are:\n %s" % pformat(dirpaths))
    return dirpaths[0]
