**************************************************
install supervisord and generate its configuration
**************************************************

|buildstatus|_

.. contents::

.. |buildstatus| image:: https://api.travis-ci.org/collective/collective.recipe.supervisor.png?branch=master
.. _buildstatus: https://travis-ci.org/collective/collective.recipe.supervisor

Detailed Documentation
**********************


This recipe when used will do the following:

* install ``supervisor`` and all its dependecies.

* generates the ``supervisord``, ``supervisorctl``, and ``memmon`` scripts in the ``bin`` directory

* generates a configuration file to be used by ``supervisord`` and ``supervisorctl`` scripts

Supported options
=================

The recipe supports the following options:

sections
    List of enabled supervisor sections.
    Defaults to enable all: ``global http ctl rpc services``.

plugins
    Extra eggs you want the recipe to install, e.g. ``superlance``

http-socket
    ``inet`` or ``unix`` socket to use for HTTP administration. Defaults to ``inet``.

file
    A path to a UNIX domain socket (e.g. ``/tmp/supervisord.sock``) on which
    supervisor will listen for HTTP/XML-RPC requests.

chmod
    Change the UNIX permission mode bits of the UNIX domain socket to this value at startup.

chown
    Change the ownership of the UNIX domain socket to this value at startup.
    Either ``user`` or ``user:group``.

port
    The port number ``supervisord`` listens to, e.g. ``9001``. Can be given as ``host:port``, e.g.
    ``127.0.0.1:9001``. Defaults to ``127.0.0.1:9001``

user
    The username required for authentication to supervisord

password
    The password required for authentication to supervisord

supervisord-conf
    Full path to where the recipe puts the supervisord configuration file.
    Defaults to ``${buildout:directory}/parts/${name}/supervisord.conf``

supervisord-user
    If supervisord is run as the root user, switch users to this UNIX user
    account before doing any meaningful processing. This value has no effect
    if supervisord is not run as root.

supervisord-directory
    When supervisord daemonizes, switch to this directory. This option can
    include the value ``%(here)s``, which expands to the directory in which the
    supervisord configuration file was found.

supervisord-environment
    A list of key/value pairs in the form ``KEY=val,KEY2=val2`` that will be placed
    in the supervisord process's environment (and as a result in all of its
    child processes' environments). This option can include the value ``%(here)s``,
    which expands to the directory in which the supervisord configuration file
    was found. Note that subprocesses will inherit the environment variables of
    the shell used to start supervisord except for the ones overridden here and
    within the program's environment configuration stanza.

childlogdir
    The full path of the directory where log files of processes managed by
    Supervisor while be stored. Defaults to ``${buildout:directory}/var/log``

logfile
    The full path to the supervisord log file. Defaults to
    ``${buildout:directory}/var/log/supervisord.log``

pidfile
    The pid file of supervisord. Defaults to
    ``${buildout:directory}/var/supervisord.pid``

logfile-maxbytes
    The maximum number of bytes that may be consumed by the activity log file
    before it is rotated. Defaults to 50MB.

logfile-backups
    The number of backups to keep around resulting from activity log file
    rotation. Defaults to 10.

loglevel
   The logging level. Can be one of ``critical``, ``error``, ``warn``, ``info``, ``debug``, ``trace``,
   or ``blather``. Defaults to ``info``.

umask
   The umask of the supervisord process. Defaults to ``022``.

nodaemon
   If true, supervisord will start in the foreground instead of daemonizing.
   Defaults to false.

nocleanup
  Prevent supervisord from clearing any existing AUTO child log files at
  startup time. Useful for debugging. Defaults to false.

serverurl
   The URL that should be used to access the supervisord server. Defaults to
   ``http://127.0.0.1:9001``

programs
   A list of programs you want the supervisord to control. One per line.
   The format of a line is as follows::

       priority process_name [(process_opts)] command [[args] [directory] [[redirect_stderr]] [user]]

   The ``[args]`` are any number of arguments you want to pass to the ``command``.
   It has to be given between ``[]`` (e.g. ``[-v fg]``). See examples below.
   If not given, ``redirect_stderr`` defaults to false.
   If not given, the ``directory`` option defaults to the directory containing the
   the command.
   The optional ``process_opts`` argument sets additional options on the proccess
   in the supervisord configuration.
   It has to be given between ``()`` and must contain options in ``key=value`` format
   with spaces only for separating options -- e.g. ``(autostart=false startsecs=10)``.
   The optional ``user`` argument gives the userid that the process should be run
   as (if supervisord is run as root).

   In most cases you will only need to give the 4 first parts::

       priority process_name command [[args]]

eventlisteners
    A list of eventlisteners you'd like supervisord to run as subprocesses to
    subscribe to event notifications. One per line. Relevant supervisor
    documentation about events is at
    http://supervisord.org/events.html ::

        processname [(process_opts)] events command [[args]]

    ``events`` is a comma-separated list (without spaces) of event type names
    that the listener is interested in receiving notifications for.

    Supervisor provides one event listener called ``memmon`` which can be used to
    restart supervisord child process once they reach a certain memory limit.
    Note that you need to define the variables ``user``, ``password`` and ``serverurl``
    (described in the supported options above) to be able to use the memmon listener.
    An example of defining a memmon event listener, which analyzes memory usage
    every 60 seconds and restarts as needed could look like::

       MemoryMonitor TICK_60 ${buildout:bin-directory}/memmon [-p process_name=200MB]

    As eventlisteners are a special case of processes, the also accept process
    options. One useful option is to start an eventlistener like the HttpOk
    checker only after your webserver has had time to start and load, say
    after 20 seconds:

       HttpOk (startsecs=20) TICK_60 ${buildout:bin-directory}/httpok [-p web -t 20 http://localhost:8080/]

groups
   A list of programs that become part of a group. One per line.
   The format of a line is as follow::

       priority group_name program_names

   ``programs_name`` is a comma-separated list of program names.

env-path
    The environment variable PATH, e.g. ``/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin``


Example
=======

::

    [buildout]
    parts = supervisor

    # ...configure zope/zeo here...

    [supervisor]
    recipe = collective.recipe.supervisor

    port = 9001
    user = johndoe
    password = secret
    serverurl = http://supervisor.johndoe.com

    plugins =
          superlance

    programs =
          10 zeo ${zeo:location}/bin/runzeo ${zeo:location}
          20 instance1 ${instance1:location}/bin/runzope ${instance1:location} true
          30 instance2 (autostart=false) ${instance2:location}/bin/runzope true
          40 maildrophost ${buildout:bin-directory}/maildropctl true
          50 other ${buildout:bin-directory}/other [-n 100] /tmp
          60 other2 ${buildout:bin-directory}/other2 [-n 100] true
          70 other3 (startsecs=10) ${buildout:bin-directory}/other3 [-n -h -v --no-detach] /tmp3 true www-data

    eventlisteners =
          Memmon TICK_60 ${buildout:bin-directory}/memmon [-p instance1=200MB]
          HttpOk (startsecs=20) TICK_60 ${buildout:bin-directory}/httpok [-p instance1 -t 20 http://localhost:8080/]

    groups =
          10 services zeo,instance1
          20 others other,other2,other3

Upgrading
=========

If upgrading from v0.19 to 0.20 the ``sections`` parameter got two new sections ``global`` and ``services``.
If ``sections`` parameter was set in old buildout config: in order to get the same behavior as before append the two new section names to value of ``sections``.

Source Code
===========

The sources are in a GIT DVCS with its main branches at `github collective <http://github.com/collective/collective.recipe.supervisor>`_.

We'd be happy to see many contributions to make it even better.
