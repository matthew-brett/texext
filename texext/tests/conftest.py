""" Skip the conf.py file in tinypages

Otherwise it gets imported twice, raises an ImportMismatchError.
"""

collect_ignore = ["conf.py"]
