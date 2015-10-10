""" Tests for tinypages build using sphinx extensions """

import shutil
import tempfile
import pickle

from os.path import (join as pjoin, dirname, isdir)

from subprocess import call, Popen, PIPE

from nose import SkipTest
from nose.tools import assert_true, assert_equal

HERE = dirname(__file__)
TINY_PAGES = pjoin(HERE, 'tinypages')


def setup():
    # Check we have the sphinx-build command
    try:
        call(['sphinx-build', '--help'], stdout=PIPE, stderr=PIPE)
    except OSError:
        raise SkipTest('Need sphinx-build on PATH for these tests')


def file_same(file1, file2):
    with open(file1, 'rb') as fobj:
        contents1 = fobj.read()
    with open(file2, 'rb') as fobj:
        contents2 = fobj.read()
    return contents1 == contents2


class TestTinyPages(object):
    # Test build and output of tinypages project

    @classmethod
    def setup_class(cls):
        cls.page_build = tempfile.mkdtemp()
        try:
            cls.html_dir = pjoin(cls.page_build, 'html')
            cls.doctree_dir = pjoin(cls.page_build, 'doctrees')
            # Build the pages with warnings turned into errors
            cmd = ['sphinx-build', '-W', '-b', 'html',
                   '-d', cls.doctree_dir,
                   TINY_PAGES,
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

    def test_some_math(self):
        assert_true(isdir(self.html_dir))
        assert_true(isdir(self.doctree_dir))
        with open(pjoin(self.doctree_dir, 'some_math.doctree'), 'rb') as fobj:
            content = fobj.read()
        doctree = pickle.loads(content)
        assert_equal(len(doctree.document), 1)
        para_strs = [str(p) for p in doctree.document[0]]
        assert_equal(
            para_strs,
            ['<title>Some math</title>',
             '<paragraph>Here <math latex="a = 1"/>, except '
             '<title_reference>$b = 2$</title_reference>.</paragraph>',
             '<paragraph>Here <math latex="a = 1"/>, except '
             '<literal>$b = 2$</literal>.</paragraph>',
             '<literal_block xml:space="preserve">Here $a = 1$</literal_block>',
             '<displaymath docname="some_math" label="None" '
             'latex="10 a + 2 b + q" nowrap="False"/>',
             '<paragraph>More text</paragraph>',
             '<target refid="equation-some-label"/>',
             '<displaymath docname="some_math" '
             """ids="[u'equation-some-label']" """
             'label="some-label" '
             'latex="5 a + 3 b" nowrap="False"/>',
             '<paragraph>Yet more text</paragraph>',
             '<displaymath docname="some_math" label="None" '
             'latex="5 w + 3 x" nowrap="False"/>'])
