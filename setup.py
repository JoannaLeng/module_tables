#!/usr/bin/env python
"""
setup.py

File for python pip install.

---------------------------------------

  Copyright (c) Joanna Leng in 2017.

  Module_table is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License v.3
  along with CPT sofware.  If not, see <http://www.gnu.org/licenses/>.

  To help us, we ask that you cite the research papers
  that are generated from this software.
"""

#from distutils.core import setup
#from setuptools import find_packages
#from setuptools import setup

#DISTUTILS_DEBUG = 1

from pathlib import Path
from setuptools import setup

def read(fname):
    """
    read and return contents of file:
        Args:
            fname (str): the file name
        Returns:
            (str) the contents of the file
    """
    return (Path(__file__).parent.joinpath(fname)).open(encoding='UTF-8').read()


setup(
    name='mt',
    version='2.0.0',
    author="Joanna Leng",
    author_email="j.leng@leeds.ac.uk",
    description='helps with web documentation of Linux systems that use modules for software.',
    long_description='Please reaad the README file inn the repositiry for more details.',
    platforms="Linux",
    url='https://github.com/JoannaLeng/module_tables/blob/master/README.md#module-table-readme',
    license='GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007',
    packages=['mt'],
    install_requires=[
        'setuptools',
        'argparse',
        'validators'
    ],
    #scripts=['module_table.py']
    entry_points={
        'console_scripts': [
            'mt = mt.module_table:main'
        ]
    }
)
