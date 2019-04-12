Change history
**************

0.21 (unreleased)
=================

- Improved code quality, fixing flake8 warning 'W605 invalid escape sequence' for regular expressions.  [maurits]

- Support the ``chown`` option in the ``unix_http_server`` section.  [guewen]

- Tested with Python 2.7, 3.6, 3.7.  [davidweterings, maurits]


0.20 (2015-10-06)
=================

- Fix tests to be able to run.
  Fixes https://github.com/collective/collective.recipe.supervisor/issues/10
  [gforcada]

- fix: memscript install script did not get conf file because of a typo.
  [moriyoshi]

- Feature: exclude global configuration so the generated file can be used
  to be included by a system wide supervisord.
  [jensens]

- Cleanup/overhaul/pep8 of code base, include self contained buildout with
  testrunner
  [jensens]


0.19 (2013-01-09)
=================

- Fix the dissapearance of dependencies from the picked eggs after the
  first run of buildout.
  [afrepues]

- Fix e-mail address in project history file, somehow it was wrong, oh
  well.
  [afrepues]


0.18 (2012-11-16)
=================

- Add travis-ci support
  [fredvd]

- Add process options to eventlisteners so you can for example delay them.
  [fredvd]

- Fix doctests, pin supervisor and superlance in the doctests
  [fredvd]

- Add support for setting user, directory and environment options of
  supervisord
  [anthonygerrard]


0.17 (2011-07-28)
====================
- Added support for process groups
  [nueces]


0.16 (2011-03-07)
=================

- Fix supervisorctl to use unix_http_server if used
  [Domen Kožar, NiteoWeb. Work sponsored by Hexagon IT]


0.15 (2011-03-05)
=================

- Added support for unix_http_server additionally to inet_http_server
  [Domen Kožar, NiteoWeb. Work sponsored by Hexagon IT]


0.14 (2010-12-10)
=================

 - Added support for the umask option of supervisord
   [afrepues@mcmaster.ca]

 - Move the credentials needed for authenticating with the supervisord
   process from the supervisorctl script to the configuration
   file. Because of bug 180705 of zc.buildout, scripts are made
   world-readable. [afrepues@mcmaster.ca]


0.13 (2010-12-07)
=================

 - 'nocleanup' option of Supervisor is now configurable from Buildout
   Patch from Damien Letournel


0.12 (2010-08-04)
=================

 - Quote the environment variables that are written in the supervisor
   configuration file for eventlisteners, otherwise supervisor will not pass
   them on correctly to for example memmon [Fred van Dijk]


0.11 (2010-08-02)
=================

 - 'childlogdir' option of Supervisor is now configurable from Buildout
   [Jonathan Ballet]

 - [include] functionnality in the supervisor configuration file.
   See http://supervisord.org/configuration.html#include
   [ycadour]


0.10.1 (2010-07-27)
===================

- Updated documentation about how to use the memmon event listener [lucielejard]


0.10 (2010-06-03)
=================

 - Added an option for the environment variable PATH
   [lucielejard]

 - Added support for disabling supervisor sections (such as http, rpc and ctl) [Domen Kozar]


0.9 (2009-11-04)
================

 - Applied Jonathan Ballet's patch: The generated control script doesn't
   automatically connect on the created supervisord when running on a custom port.


0.8 (2009-04-27)
================

 - Make it possible to set additional options per process in the control script.
   [nkryptic]


0.7 (2009-01-27)
================

 - Added 'plugins' option so we can install extra eggs (supervisor plugins)
   [mustapha]

 - Some fixes for eventlistner part [mustapha]

 - Updated tests


0.6 (2008-11-10)
================

 - One can now specify the user account that will be used as the account
   which runs the program.
   [amos]


0.5 (2008-08-23)
================

 - Adding eventlistners option for use as event notification framework.
   Targetting use with supervisor's memmon event listener
   [aburkhalter]


0.4 (2008-06-12)
================

 - Use dynamic script names to allow multiple cluster
   [gawel]

 - Ensure that the log dir is created when used without zope's recipes
   [gawel]


0.3 (2008-06-01)
================

 - Updated docs and tests
   [mustapha]

 - pep8 cosmetics
   [mustapha]

 - Make it possible to pass in arguments to the control script.
   [hannosch]

 - Put all specified options, like server url and username into the generated
   control script. This allows to run it as is.
   [hannosch]


0.2 (2008-04-23)
================

 - Make possible to pass arguments to the command so one can use ctl scripts
   with supervisor with arguments like 'fg' for zope instances or --no-detach
   or something similar for other programs
   [mustapha]

 - updated tests
   [mustapha]


0.1 (2008-04-21)
================

 - Created recipe with ZopeSkel [Mustapha Benali].
