""" Tests for tinypages build using sphinx extensions """

import shutil
import tempfile

from os.path import (join as pjoin, dirname, isdir)

from subprocess import call, Popen, PIPE

from nose import SkipTest
from nose.tools import assert_true

HERE = dirname(__file__)
TINY_PAGES = pjoin(HERE, 'tinypages')


def setup():
    # Check we have the sphinx-build command
    try:
        ret = call(['sphinx-build', '--help'], stdout=PIPE, stderr=PIPE)
    except OSError:
        raise SkipTest('Need sphinx-build on path for these tests')
    if ret != 0:
        raise RuntimeError('sphinx-build does not return 0')


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

        def plot_file(num):
            return pjoin(self.html_dir, 'some_plots-{0}.png'.format(num))

        with open(pjoin(self.html_dir, 'some_math.html'), 'rt') as fobj:
            html_contents = [line.strip() for line in fobj]
        assert_true('<p>Here <span class="math">\(a = 1\)</span>, except '
                    '<cite>$b = 2$</cite>.</p>' in html_contents)
        assert_true('<p>Here <span class="math">\(a = 1\)</span>, except '
                    '<code class="docutils literal">'
                    '<span class="pre">$b</span> '
                    '<span class="pre">=</span> <span class="pre">2$</span>'
                    '</code>.</p>' in html_contents)
        assert_true('<div class="highlight-python"><div class="highlight">'
                    '<pre>Here $a = 1$' in html_contents)
        assert_true(r'\[10 a + 2 b\]</div>' in html_contents)
