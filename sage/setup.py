## -*- encoding: utf-8 -*-
"""
Harvesting and exporting metadata from Sage by introspection
"""

import os
import sys
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
# To use a consistent encoding
from codecs import open

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, '../README.md'), encoding='utf-8') as f:
    long_description = f.read()

class SageTest(TestCommand):
    def run_tests(self):
        errno = os.system("sage -t --force-lib sagetypes.py")
        sys.exit(errno)

setup(
    name='sage-export-metadata',
    version='0.1.0',
    description='Sage Metadata exporter',
    long_description=long_description,
    url='...',
    author='Nicolas M. Thiéry',
    author_email='nthiery@users.sf.net',
    license='GPLv2+',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research'
        'Topic :: Software Development :: Build Tools',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 2',
        #'Programming Language :: Python :: 3',
    ],
    keywords='SageMath',
    packages=find_packages(),
    install_requires = ['scscp','openmath>=0.2.1','sage-gap-semantic-interface'], # openmath
    dependency_links=['https://github.com/nthiery/sage-gap-semantic-interface/tarball/master#egg=sage-gap-semantic-interface-0.1.0',
                      'https://github.com/OpenMath/py-openmath/tarball/convert-pickle#egg=openmath-0.2.1'
                     ], # 'Sage'
    cmdclass = {'test': SageTest},
)
