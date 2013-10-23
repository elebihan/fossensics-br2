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
Collect FOSS information after a Buildroot build
"""

import os
import re
import subprocess
import tempfile
from collections import namedtuple
from gettext import gettext as _

Statistics = namedtuple('Statistics',
                        ('n_progs', 'n_packages', 'n_orphans', 'n_undocs',
                         'package_stats'))

class ToolNotFoundError(Exception):
    """Error raised when a program is not found in $PATH"""

def _find_strip(directory):
    bindir = os.path.join(directory, 'host', 'usr', 'bin')
    for fn in os.listdir(bindir):
        fn = os.path.join(bindir, fn)
        if os.path.isfile(fn) and os.access(fn, os.X_OK):
            if fn.endswith('-strip'):
                return fn
    raise ToolNotFoundError(_("Can not find 'strip' program"))

class Inspector(object):
    def __init__(self, builddir):
        self._buildir = builddir
        self._rootdir = os.path.join(self._buildir, 'target')
        strip = _find_strip(builddir)
        opts = '--remove-section=.comment --remove-section=.note -R .note.GNU-stack'
        self._strip_cmd = strip + ' ' + opts
        self._n_progs = 0
        self._n_orphans = 0
        self._n_undocs = 0
        self._pkg_stats = {}

    def inspect(self, destination):
        if not os.path.exists(destination):
            os.makedirs(destination)
        progs_fn = self._collect_progs(destination)
        self._collect_deps(progs_fn, destination)
        origs_fn, orphs_fn = self._collect_origins(progs_fn, destination)
        pkgs_fn = self._refine_origins(origs_fn, destination)
        lics_fn, undocs_fn = self._collect_licenses(pkgs_fn, destination)
        self._compute_stats(pkgs_fn, orphs_fn, undocs_fn)

    def _collect_progs(self, destination):
        outfn = os.path.join(destination, 'progs.txt')
        args = ('grissom-scan', self._rootdir)
        with open(outfn, 'w') as f:
            subprocess.check_call(args, stdout=f)
        return outfn

    def _collect_deps(self, infn, destination):
        outfn = os.path.join(destination, 'deps.txt')
        args = ('grissom-deps',
                '-L', os.path.join(self._rootdir, 'lib'),
                '-L', os.path.join(self._rootdir, 'usr', 'lib'),
                '-D', '-f', 'simple', '-')
        with open(infn, 'r') as inf:
            with open(outfn, 'w') as outf:
                subprocess.check_call(args, stdin=inf, stdout=outf)
        return outfn

    def _collect_origins(self, infn, destination):
        outfn = os.path.join(destination, 'origins.txt')
        errfn = os.path.join(destination, 'orphans.txt')
        args = ('grissom-origin', '-Q',
                '-I', os.path.join(self._buildir, 'build'),
                '-S', self._strip_cmd, '-')
        with open(infn, 'r') as inf:
            with open(outfn, 'w') as outf:
                with open(errfn, 'w') as errf:
                    subprocess.call(args,
                                    stdin=inf,
                                    stdout=outf,
                                    stderr=errf)
        return outfn, errfn

    def _refine_origins(self, infn, destination):
        outfn = os.path.join(destination, 'packages.txt')
        builddir = os.path.join(self._buildir, 'build')
        with open(infn, 'r') as inf:
            with open(outfn, 'w') as outf:
                for line in inf:
                    fn, dn = line.strip().split(': ')
                    path = dn.replace(builddir, '')
                    pkg = path.split(os.sep)[1]
                    newline = "{0}\t{1}\n".format(pkg, fn)
                    outf.write(newline)
        return outfn

    def _collect_licenses(self, infn, destination):
        outfn = os.path.join(destination, 'licenses.txt')
        errfn = os.path.join(destination, 'undocumented.txt')
        args = ('grissom-legal-info', 'query', '-')
        packages = []
        with open(infn, 'r') as inf:
            for line in inf:
                package, program = line.split()
                packages.append(package)
        with tempfile.NamedTemporaryFile() as tmpf:
            for package in sorted(set(packages)):
                tmpf.write("{}%\n".format(package).encode('utf-8'))
            tmpf.seek(0)
            with open(outfn, 'w') as outf:
                with open(errfn, 'w') as errf:
                    subprocess.call(args,
                                    stdin=tmpf,
                                    stdout=outf,
                                    stderr=errf)
        return outfn, errfn

    def _compute_stats(self, packages_fn, orphans_fn, undocs_fn):
        with open(orphans_fn, 'r') as f:
            for line in f:
                self._n_orphans += 1
        with open(packages_fn, 'r') as f:
            for line in f:
                pkg, prog = line.strip().split()
                if pkg in self._pkg_stats.keys():
                    self._pkg_stats[pkg] += 1
                else:
                    self._pkg_stats[pkg] = 1
                self._n_progs += 1
        with open(undocs_fn, 'r') as f:
            expr = re.compile(r'\'(.+)%\'')
            for line in f:
                if expr.search(line):
                    self._n_undocs += 1

    @property
    def statistics(self):
        pkg_stats = [(p, c) for p, c in self._pkg_stats.items()]
        pkg_stats.sort(key=lambda stats: stats[1], reverse=True)
        return Statistics(self._n_progs,
                          len(self._pkg_stats.keys()),
                          self._n_orphans,
                          self._n_undocs,
                          pkg_stats)

def format_statistics(stats):
    """Format statistics.

    :param statistics: statistics.
    :type statistics: :class:`fossensics.buildroot2.Statistics`
    """
    msg = _('Global Statistics')
    print("{0}\n{1}\n".format(msg, '-' * len(msg)))
    print(_("Number of packages: {0}").format(stats.n_packages))
    print(_("Number of programs: {0}").format(stats.n_progs))
    print(_("Number of orphans: {0}").format(stats.n_orphans))
    print(_("Number of undocumented: {0}\n").format(stats.n_undocs))

    msg = _('Packages Statistics')
    print("{0}\n{1}\n".format(msg, '-' * len(msg)))
    print(_("Here is the number of programs provided by each package:\n"))
    for p, c in stats.package_stats:
        print("- {0:<24} {1}".format(p, c))

# vim: ts=4 sts=4 sw=4 et ai
