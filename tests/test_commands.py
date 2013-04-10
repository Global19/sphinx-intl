# -*- coding: utf-8 -*-
"""
    test_commands
    ~~~~~~~~~~~~~

    Test all commands that have no special checks.

    :copyright: Copyright 2013 by Takayuki SHIMIZUKAWA.
    :license: BSD, see LICENSE for details.
"""

import os
import shutil
import tempfile
from functools import wraps

from nose import SkipTest
from nose.tools import raises
from six import PY3

from sphinx_intl import commands

__dir__ = os.path.dirname(os.path.abspath(__file__))


def in_tmp(template_dir='root', **kwargs):
    def generator(func):
        @wraps(func)
        def deco(*args2, **kwargs2):
            tempdir = tempfile.mkdtemp()
            shutil.copytree(
                os.path.join(__dir__, template_dir),
                os.path.join(tempdir, template_dir))
            cwd = os.getcwd()
            try:
                os.chdir(os.path.join(tempdir, template_dir))
                func(*args2, **kwargs2)
                shutil.rmtree(tempdir, ignore_errors=True)
            finally:
                os.chdir(cwd)
        return deco
    return generator


def teardown_module():
    pass


@raises(SystemExit)
@in_tmp()
def test_command_not_found():
    commands.parse_option(['some-command'])


@raises(RuntimeError)
@in_tmp()
def test_confpy_not_have_locale_dirs():
    f = open('conf.py', 'w')
    f.close()
    commands.parse_option(['update'])


@in_tmp()
def test_confpy_have_locale_dirs():
    f = open('conf.py', 'w')
    f.write('locale_dirs=["somedir"]\n')
    f.close()
    opts, args = commands.parse_option(['update'])
    assert opts.locale_dir == 'somedir'


@in_tmp()
def test_confpy_in_subdir():
    os.mkdir('source')
    f = open('source/conf.py', 'w')
    f.write('locale_dirs=["somedir"]\n')
    f.close()
    opts, args = commands.parse_option(['update', '-c', 'source/conf.py'])
    assert opts.locale_dir == 'somedir'


@in_tmp()
def test_no_confpy_and_locale_dir_specified():
    opts, args = commands.parse_option(['update', '-d', 'somedir'])
    assert opts.locale_dir == 'somedir'


@raises(RuntimeError)
@in_tmp()
def test_update_pot_notfound():
    commands.update('locale')


@in_tmp()
def test_update():
    commands.update('locale', '_build/locale')


@in_tmp()
def test_build():
    commands.build('locale')


@in_tmp()
def test_create_transifexrc():
    if PY3:
        raise SkipTest('transifex-client not support Python3')
    commands.create_transifexrc('spam-id', 'egg-pw')


@in_tmp()
def test_create_txconfig():
    if PY3:
        raise SkipTest('transifex-client not support Python3')
    commands.create_txconfig()


@in_tmp()
def test_update_txconfig_resources():
    if PY3:
        raise SkipTest('transifex-client not support Python3')
    commands.create_txconfig()
    commands.update_txconfig_resources('ham-project', 'locale')
