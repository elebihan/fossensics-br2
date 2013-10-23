==============
fossensics-br2
==============

------------------------------------------------
Collect FOSS information after a Buildroot build
------------------------------------------------

:Author: Eric Le Bihan <eric.le.bihan.dev@free.fr>
:Copyright: 2013 Eric Le Bihan
:Manual section: 1

SYNOPSIS
========

fossensics-br2 [OPTIONS] <builddir>

DESCRIPTION
===========

`fossensics-br2` collects FOSS information after a Buildroot build, which
occured in the *builddir* directory. It is mainly a wrapper around the
grissom-* tools.

Several files are generated in the current directory (or the one specified
using *--output* option):

- progs.txt: programs available in the target file system.
- deps.txt: dependency list for the programs found.
- origins.txt: mapping between the programs and their source package.
- orphans.txt: programs which source package could not be found.
- packages.txt: mapping between the source packages and the programs.
- licenses.txt: licensing information for each source package.
- undocumented.txt: source packages without licensing information.

Some statistics can be displayed if the *--stats* option is set.

OPTIONS
=======

-o DIR, --output DIR        set output directory
-s, --stats                 display statistics when finished

SEE ALSO
========

- `grissom-deps(1)`
- `grissom-scan(1)`
- `grissom-legal-info(1)`

.. vim: ft=rst
