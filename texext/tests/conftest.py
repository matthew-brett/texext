""" Configuration for py.test test run
"""

def pytest_ignore_collect(path, config):
    """ Skip the conf.py file in tinypages

    Otherwise it gets imported twice, raises an ImportMismatchError.
    """
    return path.basename == 'conf.py'
