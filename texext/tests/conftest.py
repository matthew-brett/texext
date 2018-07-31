""" Skip the conf.py file in tinypages

Otherwise it gets imported twice, raises an ImportMismatchError.
"""

from os.path import join as pjoin

collect_ignore = [pjoin('tinypages', "conf.py")]
