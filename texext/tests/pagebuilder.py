""" Tests for tinypages build using sphinx extensions """

import shutil
import tempfile

from os.path import join as pjoin

from subprocess import call, Popen, PIPE

from nose import SkipTest


def setup_module():
    try:
        call(['sphinx-build', '--help'], stdout=PIPE, stderr=PIPE)
    except OSError:
        raise SkipTest('Need sphinx-build on PATH for these tests')


class PageBuilder(object):
    """ Class to build sphinx pages in temporary directory """
    page_path = None

    @classmethod
    def setup_class(cls):
        cls.page_build = tempfile.mkdtemp()
        try:
            cls.html_dir = pjoin(cls.page_build, 'html')
            cls.doctree_dir = pjoin(cls.page_build, 'doctrees')
            # Build the pages with warnings turned into errors
            cmd = ['sphinx-build', '-W', '-b', 'html',
                   '-d', cls.doctree_dir,
                   cls.page_path,
                   cls.html_dir]
            proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
            out, err = proc.communicate()
        except Exception as e:
            shutil.rmtree(cls.page_build)
            raise e
        if proc.returncode != 0:
            shutil.rmtree(cls.page_build)
            raise RuntimeError('sphinx-build failed with stdout:\n'
                               '{0}\nstderr:\n{1}\n'.format(
                                    out, err))

    @classmethod
    def teardown_class(cls):
        shutil.rmtree(cls.page_build)
