# -*- coding: utf-8 -*-
"""
This module contains the tool of collective.recipe.supervisor
"""
from setuptools import find_packages
from setuptools import setup

import os


def read(path):
    with open(path, 'rb') as filepath:
        return filepath.read().decode('utf-8')


version = '1.0.1.dev0'

long_description = (
    read('README.rst')
    + '\n\n'
    + read('CHANGES.rst')
    + '\n\n'
    + read('CONTRIBUTORS.rst')
)

entry_point = 'collective.recipe.supervisor:Recipe'
entry_points = {"zc.buildout": ["default = %s" % entry_point]}

tests_require = ['zc.buildout[test]']

setup(
    name='collective.recipe.supervisor',
    version=version,
    description="A buildout recipe to install supervisor",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers
    classifiers=[
        'Development Status :: 6 - Mature',
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='buildout recipe supervisor',
    author='Mustapha Benali',
    author_email='mustapha@headnet.dk',
    url='https://github.com/collective/collective.recipe.supervisor/',
    license='ZPL',
    packages=find_packages(),
    namespace_packages=['collective', 'collective.recipe'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'zc.buildout',
        'zc.recipe.egg',
    ],
    tests_require=tests_require,
    extras_require=dict(test=tests_require),
    test_suite='collective.recipe.supervisor.tests.test_docs.test_suite',
    entry_points=entry_points,
)
