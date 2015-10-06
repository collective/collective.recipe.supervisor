# -*- coding: utf-8 -*-
"""
This module contains the tool of collective.recipe.supervisor
"""
from setuptools import find_packages
from setuptools import setup

import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.20'

long_description = (
    read('README.rst') + '\n\n' +
    read('docs', 'CHANGES.rst') + '\n\n' +
    read('docs', 'CONTRIBUTORS.rst')
)

entry_point = 'collective.recipe.supervisor:Recipe'
entry_points = {"zc.buildout": ["default = %s" % entry_point]}

tests_require = ['zc.buildout[test]']

setup(name='collective.recipe.supervisor',
      version=version,
      description="A buildout recipe to install supervisor",
      long_description=long_description,
      # Get more: from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Framework :: Buildout',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'License :: OSI Approved :: Zope Public License',
      ],
      keywords='buildout recipe supervisor',
      author='Mustapha Benali',
      author_email='mustapha@headnet.dk',
      url='http://pypi.python.org/pypi/collective.recipe.supervisor',
      license='ZPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.recipe'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'zc.buildout',
                        'zc.recipe.egg',
                        # -*- Extra requirements: -*-
                        ],
      tests_require=tests_require,
      extras_require=dict(test=tests_require),
      test_suite='collective.recipe.supervisor.tests.test_docs.test_suite',
      entry_points=entry_points,
      )
