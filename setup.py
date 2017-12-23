"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README'), encoding='utf-8') as f:
    long_description = f.read()

about = {}
with open(path.join(here, 'ReadEm', '__version__.py'), 'r', 'utf-8') as f:
    exec(f.read(), about)

setup(
    name=about['__title__'], 
    version=about['__version__'],
    description=about['__description__'],
    long_description=long_description,
    url=about['__url__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    license=about['__license__'],

    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'Topic :: Software Development :: Documentation',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Wiki',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Text Processing',
        'Topic :: Utilities',

        # Pick your license as you wish
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='readme markdown documentation',  # Optional
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required

    install_requires=['Markdown'],  # Optional
    python_requires='>=3',
    include_package_data=True,
    #exclude_package_data={'Note': ['Note']},

    # List additional groups of dependencies here (e.g. development
    # dependencies). Users will be able to install these using the "extras"
    # syntax, for example:
    #   $ pip install sampleproject[dev]
    # Similar to `install_requires` above, these must be valid existing
    # projects.
    #extras_require={  # Optional
    #    'dev': ['check-manifest'],
    #    'test': ['coverage'],
    #},

)