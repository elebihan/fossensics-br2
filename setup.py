# -*- coding: utf-8 -*-
#
# fossensics-br2 - Collect FOSS information from a Buildroot build
#
# Copyright (c) 2013 Eric Le Bihan <eric.le.bihan.dev@free.fr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from distutils.core import setup
from disthelpers import build, build_trans, build_man, install_data
from fossensics import __version__

setup(name='fossensics-br2',
      version=__version__,
      description='Collect FOSS information from a Buildroot build',
      long_description='''
      This program inspect the root file system created using Buildroot to
      collect FOSS related information.
      ''',
      license='GPLv3',
      url='https://github.com/elebihan/fossensics-br2/',
      platforms=['linux'],
      classifiers=('Programming Language :: Python :: 3',
                   'Intended Audience :: Developers',
                   'Natural Language :: English'
                   'License :: OSI Approved :: GNU General Public License (GPL)',),
      keywords=['buildroot', 'FOSS'],
      requires=['docutils (>=0.11)'],
      packages=['fossensics'],
      scripts=['scripts/fossensics-br2'],
      data_files=[('share/man/man1', ['build/man/man1/fossensics-br2.1'])],
      author='Eric Le Bihan',
      author_email='eric.le.bihan.dev@free.fr',
      cmdclass = {'build': build,
                  'build_man': build_man,
                  'build_trans': build_trans,
                  'install_data': install_data})

# vim: ts=4 sts=4 sw=4 sta et ai
