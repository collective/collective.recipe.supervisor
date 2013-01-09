# -*- coding: utf-8 -*-
"""Recipe supervisor"""

import os
import re
import zc.recipe.egg


class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options

        if self.options.get('supervisord-conf') is None:
            self.options['supervisord-conf'] = os.path.join(
                self.buildout['buildout']['parts-directory'],
                self.name,
                'supervisord.conf',
                )

    def install(self):
        """Installer"""
        # XXX Implement recipe functionality here
        # Return files that were created by the recipe. The buildout
        # will remove all returned files upon reinstall.

        # general options
        sections = self.options.get('sections', 'ctl http rpc').split()

        # supervisord
        buildout_dir = self.buildout['buildout']['directory']
        logfile = self.options.get('logfile', os.path.join(buildout_dir,
                                                           'var',
                                                           'log',
                                                           'supervisord.log'))
        pidfile = self.options.get('pidfile', os.path.join(buildout_dir,
                                                           'var',
                                                           'supervisord.pid'))
        childlogdir = self.options.get('childlogdir', os.path.join(buildout_dir,
                                                           'var',
                                                           'log'))
        log_dir = os.path.abspath(os.path.dirname(logfile))
        pid_dir = os.path.abspath(os.path.dirname(pidfile))
        http_socket = self.options.get('http-socket', 'inet')
        logfile_maxbytes = self.options.get('logfile-maxbytes', '50MB')
        logfile_backups = self.options.get('logfile-backups', '10')
        loglevel = self.options.get('loglevel', 'info')
        umask = self.options.get('umask', '022')
        nodaemon = self.options.get('nodaemon', 'false')
        nocleanup = self.options.get('nocleanup', 'false')

        def option_setting(options, key, supervisor_key):
            return options.get(key, False) \
                and ('%s = %s' % (supervisor_key, options.get(key))) \
                or ''

        supervisord_user = option_setting(self.options, 'supervisord-user', 'user')
        supervisord_directory = option_setting(self.options, 'supervisord-directory', 'directory')
        supervisord_environment = option_setting(self.options, 'supervisord-environment', 'environment')

        config_data = CONFIG_TEMPLATE % locals()

        # environment PATH variable
        env_path = self.options.get('env-path', None)
        if env_path is not None:
            config_data += PATH_TEMPLATE % locals()

        # make dirs
        for folder in [childlogdir, log_dir, pid_dir]:
            if not os.path.isdir(folder):
                os.makedirs(folder)

        # (unix|inet)_http_server
        port = self.options.get('port', '127.0.0.1:9001')
        user = self.options.get('user', '')
        password = self.options.get('password', '')
        if 'http' in sections:
            if http_socket == 'inet':
                config_data += INET_HTTP_TEMPLATE % locals()
            elif http_socket == 'unix':
                file_ = self.options.get('file', '')
                chmod = self.options.get('chmod', '0700')
                config_data += UNIX_HTTP_TEMPLATE % locals()
            else:
                raise ValueError("http-socket only supports values inet or unix.")

        # supervisorctl
        if http_socket == 'inet':
            if ':' in port:
                default_serverhost = port
            else:
                default_serverhost = 'localhost:%s' % port
            default_serverhost = 'http://%s' % default_serverhost
        elif http_socket == 'unix':
            default_serverhost = 'unix://%s' % file_
        serverurl = self.options.get('serverurl', default_serverhost)
        if 'ctl' in sections:
            config_data += CTL_TEMPLATE % locals()

        # rpc
        if 'rpc' in sections:
            config_data += RPC_TEMPLATE % locals()

        # programs
        programs = [p for p in self.options.get('programs', '').splitlines() if p]
        pattern = re.compile("(?P<priority>\d+)"
                             "\s+"
                             "(?P<processname>[^\s]+)"
                             "(\s+\((?P<processopts>([^\)]+))\))?"
                             "\s+"
                             "(?P<command>[^\s]+)"
                             "(\s+\[(?P<args>(?!true|false)[^\]]+)\])?"
                             "(\s+(?P<directory>(?!true|false)[^\s]+))?"
                             "(\s+(?P<redirect>(true|false)))?"
                             "(\s+(?P<user>[^\s]+))?")

        for program in programs:
            match = pattern.match(program)
            if not match:
                raise ValueError("Program line incorrect: %s" % program)

            parts = match.groupdict()
            program_user = parts.get('user')
            process_options = parts.get('processopts')
            extras = []

            if program_user:
                extras.append('user = %s' % program_user)
            if process_options:
                for part in process_options.split():
                    if part.find('=') == -1:
                        continue
                    (key, value) = part.split('=', 1)
                    if key and value:
                        extras.append("%s = %s" % (key, value))

            config_data += PROGRAM_TEMPLATE % \
                           dict(program = parts.get('processname'),
                                command = parts.get('command'),
                                priority = parts.get('priority'),
                                redirect_stderr = parts.get('redirect') or \
                                                  'false',
                                directory = parts.get('directory') or \
                                         os.path.dirname(parts.get('command')),
                                args = parts.get('args') or '',
                                extra_config = "\n".join(extras),
                           )

        # eventlisteners
        eventlisteners = [e for e in self.options.get('eventlisteners', '').splitlines()
                            if e]

        pattern = re.compile("(?P<processname>[^\s]+)"
                             "(\s+\((?P<processopts>([^\)]+))\))?"
                             "\s+"
                             "(?P<events>[^\s]+)"
                             "\s+"
                             "(?P<command>[^\s]+)"
                             "(\s+\[(?P<args>[^\]]+)\])?")

        for eventlistener in eventlisteners:
            match = pattern.match(eventlistener)
            if not match:
                raise ValueError("Event Listeners line incorrect: %s" % eventlistener)

            parts = match.groupdict()
            process_options = parts.get('processopts')
            extras = []

            if process_options:
                for part in process_options.split():
                    if part.find('=') == -1:
                        continue
                    (key, value) = part.split('=', 1)
                    if key and value:
                        extras.append("%s = %s" % (key, value))

            config_data += EVENTLISTENER_TEMPLATE % \
                           dict(name = parts.get('processname'),
                                events = parts.get('events'),
                                command = parts.get('command'),
                                args = parts.get('args'),
                                user = user,
                                password = password,
                                serverurl = serverurl,
                                extra_config = "\n".join(extras),
                           )

        # groups
        groups = [g for g in self.options.get('groups', '').splitlines() if g]

        pattern = re.compile("(?P<priority>\d+)"
                             "\s+"
                             "(?P<group>[^\s]+)"
                             "\s+"
                             "(?P<programs>[^\s]+)")

        for group in groups:
            match = pattern.match(group)
            if not match:
                raise ValueError("Group line incorrect: %s" % group)

            parts = match.groupdict()

            config_data += GROUP_TEMPLATE % \
                           dict(priority = parts.get('priority'),
                                group = parts.get('group'),
                                programs = parts.get('programs'),
                           )

        # include
        files = [f for f in self.options.get('include', '').splitlines() if f]
        if files:
            stringfiles = " ".join(files)
            config_data += INCLUDE_TEMPLATE % \
                           dict(stringfiles=stringfiles,
                                )

        conf_file = self.options.get('supervisord-conf')

        if not os.path.exists(os.path.dirname(conf_file)):
            os.makedirs(os.path.dirname(conf_file))

        open(conf_file, 'w').write(config_data)

        return self._install_scripts()

    def _install_scripts(self):
        conf_file = self.options.get('supervisord-conf')

        init_stmt = 'import sys; sys.argv.extend(["-c","%s"])' % \
            (conf_file,)
        dscript = zc.recipe.egg.Egg(
            self.buildout,
            self.name,
            {'eggs': 'supervisor',
             'scripts': 'supervisord=%sd' % self.name,
             'initialization': init_stmt,
             })

        memscript = zc.recipe.egg.Egg(
            self.buildout,
            self.name,
            {'eggs': 'supervisor',
             'scripts': 'memmon=memmon',
             })

        init_stmt = 'import sys; sys.argv[1:1] = ["-c","%s"]' % \
            (conf_file,)
        ctlscript = zc.recipe.egg.Egg(
            self.buildout,
            self.name,
            {'eggs': 'supervisor',
             'scripts': 'supervisorctl=%sctl' % self.name,
             'initialization': init_stmt,
             'arguments': 'sys.argv[1:]',
             })

        #install extra eggs if any
        eggs = self.options.get('plugins', '')

        extra_eggs = []
        if eggs:
            extra_eggs = list(
                zc.recipe.egg.Egg(
                    self.buildout,
                    self.name,
                    {'eggs': eggs,
                     }).install())

        return list(dscript.install()) + \
               list(memscript.install()) + \
               list(ctlscript.install()) + \
               extra_eggs + \
               [conf_file]

    def update(self):
        """Updater"""
        return self._install_scripts()


CONFIG_TEMPLATE = """
[supervisord]
childlogdir = %(childlogdir)s
logfile = %(logfile)s
logfile_maxbytes = %(logfile_maxbytes)s
logfile_backups = %(logfile_backups)s
loglevel = %(loglevel)s
pidfile = %(pidfile)s
umask = %(umask)s
nodaemon = %(nodaemon)s
nocleanup = %(nocleanup)s
%(supervisord_user)s
%(supervisord_directory)s
%(supervisord_environment)s
"""

PATH_TEMPLATE = """\
environment=PATH=%(env_path)s
"""

CTL_TEMPLATE = """
[supervisorctl]
serverurl = %(serverurl)s
username = %(user)s
password = %(password)s
"""

INET_HTTP_TEMPLATE = """
[inet_http_server]
port = %(port)s
username = %(user)s
password = %(password)s
"""

UNIX_HTTP_TEMPLATE = """
[unix_http_server]
file = %(file_)s
username = %(user)s
password = %(password)s
chmod = %(chmod)s
"""

RPC_TEMPLATE = """
[rpcinterface:supervisor]
supervisor.rpcinterface_factory=supervisor.rpcinterface:make_main_rpcinterface
"""

PROGRAM_TEMPLATE = """
[program:%(program)s]
command = %(command)s %(args)s
process_name = %(program)s
directory = %(directory)s
priority = %(priority)s
redirect_stderr = %(redirect_stderr)s
%(extra_config)s
"""

EVENTLISTENER_TEMPLATE = """
[eventlistener:%(name)s]
command = %(command)s %(args)s
events = %(events)s
process_name=%(name)s
environment=SUPERVISOR_USERNAME='%(user)s',SUPERVISOR_PASSWORD='%(password)s',SUPERVISOR_SERVER_URL='%(serverurl)s'
%(extra_config)s
"""

GROUP_TEMPLATE = """
[group:%(group)s]
programs = %(programs)s
priority = %(priority)s
"""

INCLUDE_TEMPLATE = """
[include]
files = %(stringfiles)s
"""
