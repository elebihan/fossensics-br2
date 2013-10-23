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

"""
Collect FOSS information after a build
"""

__version__ = '0.1.0'

import os
import sys
from gettext import bindtextdomain, textdomain

def setup_i18n():
    """Set up internationalization."""
    if hasattr(sys, 'frozen'):
        root_dir = os.path.dirname(sys.executable)
    else:
        root_dir = os.path.dirname(os.path.abspath(__file__))
    if 'lib' not in root_dir:
        return
    root_dir, mod_dir = root_dir.split('lib', 1)
    locale_dir = os.path.join(root_dir, 'share', 'locale')

    bindtextdomain('fossensics', locale_dir)
    textdomain('fossensics')

# vim: ts=4 sts=4 sw=4 et ai
