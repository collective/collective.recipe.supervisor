"""
This module contains the tool of collective.recipe.supervisor
"""
from setuptools import setup


def read(path):
    with open(path, encoding='utf-8') as filepath:
        return filepath.read()


version = '2.0.0'

long_description = (
    read('README.rst')
    + '\n\n'
    + read('CHANGES.rst')
    + '\n\n'
    + read('CONTRIBUTORS.rst')
)

entry_point = 'collective.recipe.supervisor:Recipe'
entry_points = {"zc.buildout": ["default = %s" % entry_point]}

tests_require = [
    'zc.buildout[test]',
    'zope.testrunner',
]

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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.10',
    keywords='buildout recipe supervisor',
    author='Mustapha Benali',
    author_email='mustapha@headnet.dk',
    url='https://github.com/collective/collective.recipe.supervisor/',
    license='ZPL',
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'zc.buildout',
        'zc.recipe.egg',
    ],
    tests_require=tests_require,
    extras_require=dict(test=tests_require),
    test_suite='collective.recipe.supervisor.tests.test_docs.test_suite',
    entry_points=entry_points,
)
