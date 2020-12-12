#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


import glob
import os
from os.path import abspath, dirname, normpath
import shutil
from setuptools import setup, Command


here = normpath(abspath(dirname(__file__)))


class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    CLEAN_FILES = './build ./dist ./*.pyc ./*.tgz src/*.egg-info'.split(' ')

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        global here

        for path_spec in self.CLEAN_FILES:
            # Make paths absolute and relative to this path
            abs_paths = glob.glob(os.path.normpath(
                os.path.join(here, path_spec)))
            for path in [str(p) for p in abs_paths]:
                if not path.startswith(here):
                    # Die if path in CLEAN_FILES is absolute + outside this directory
                    raise ValueError(
                        "%s is not a path inside %s" % (path, here))
                print('removing %s' % os.path.relpath(path))
                shutil.rmtree(path)


setup(
    name='powerline-k8sstatus',
    description='A Powerline segment for showing the status of current Kubernetes context',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    version='1.0.2',
    keywords='powerline k8s kubernetes status prompt',
    license='MIT',
    author='Jose Angel Munoz',
    author_email='josea.munoz@gmail.com',
    url='https://github.com/imjoseangel/powerline-k8sstatus',
    packages=['powerline_k8sstatus'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Terminals',
        'Topic :: Utilities'
    ],
    install_requires=[
        "kubernetes"
    ],
    cmdclass={
        'clean': CleanCommand,
    }
)
