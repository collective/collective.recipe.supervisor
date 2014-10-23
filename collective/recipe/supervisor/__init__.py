# -*- coding: utf-8 -*-
"""Recipe supervisor"""
from collective.recipe.supervisor import templates

import os
import re
import zc.recipe.egg


def option_setting(options, key, supervisor_key):
    return options.get(key, False) \
        and ('%s = %s' % (supervisor_key, options.get(key))) \
        or ''


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

    @property
    def _sections(self):
        default = 'global ctl http rpc services'

        return self.options.get('sections', default).split()

    def install(self):
        """Installer"""
        # Return files that were created by the recipe. The buildout
        # will remove all returned files upon reinstall.

        # general options
        buildout_dir = self.buildout['buildout']['directory']

        config_data = ""

        param = dict()

        param['user'] = self.options.get('user', '')
        param['password'] = self.options.get('password', '')
        param['port'] = self.options.get('port', '127.0.0.1:9001')
        param['file'] = self.options.get('file', '')
        param['chmod'] = self.options.get('chmod', '0700')
        if self.options.get('chown'):
            param['chown'] = 'chown = %s' % self.options['chown']
        else:
            param['chown'] = ''

        http_socket = self.options.get('http-socket', 'inet')
        host_default = param['port']
        if http_socket == 'inet':
            if ':' not in host_default:
                host_default = 'localhost:{0}'.format(host_default)
            host_default = 'http://{0}'.format(host_default)
        elif http_socket == 'unix':
            host_default = 'unix://%s' % param['file']

        param['serverurl'] = self.options.get('serverurl', host_default)

        if 'global' in self._sections:
            # supervisord service
            param['logfile'] = self.options.get(
                'logfile',
                os.path.join(buildout_dir, 'var', 'log', 'supervisord.log')
            )
            param['pidfile'] = self.options.get(
                'pidfile',
                os.path.join(buildout_dir, 'var', 'supervisord.pid')
            )
            param['childlogdir'] = self.options.get(
                'childlogdir',
                os.path.join(buildout_dir, 'var', 'log')
            )
            if not os.path.isdir(param['childlogdir']):
                os.makedirs(param['childlogdir'])

            param['log_dir'] = os.path.abspath(
                os.path.dirname(param['logfile'])
            )
            if not os.path.isdir(param['log_dir']):
                os.makedirs(param['log_dir'])

            param['pid_dir'] = os.path.abspath(
                os.path.dirname(param['logfile'])
            )
            if not os.path.isdir(param['pid_dir']):
                os.makedirs(param['pid_dir'])

            param['logfile_maxbytes'] = self.options.get(
                'logfile-maxbytes',
                '50MB'
            )
            param['logfile_backups'] = self.options.get(
                'logfile-backups',
                '10'
            )
            param['loglevel'] = self.options.get('loglevel', 'info')
            param['umask'] = self.options.get('umask', '022')
            param['nodaemon'] = self.options.get('nodaemon', 'false')
            param['nocleanup'] = self.options.get('nocleanup', 'false')

            param['supervisord_user'] = option_setting(
                self.options,
                'supervisord-user',
                'user'
            )
            param['supervisord_directory'] = option_setting(
                self.options,
                'supervisord-directory',
                'directory'
            )
            param['supervisord_environment'] = option_setting(
                self.options,
                'supervisord-environment',
                'environment'
            )
            config_data += templates.GLOBAL % param

            # environment PATH variable
            env_path = self.options.get('env-path', None)
            if env_path is not None:
                config_data += templates.PATH % locals()

        if 'ctl' in self._sections:
            # (unix|inet)_http_server
            if 'http' in self._sections:
                if http_socket == 'inet':
                    config_data += templates.INET_HTTP % param
                elif http_socket == 'unix':
                    config_data += templates.UNIX_HTTP % param
                else:
                    raise ValueError(
                        "http-socket only supports values inet or nix."
                    )

            # supervisorctl
            config_data += templates.CTL % param

        # rpc
        if 'rpc' in self._sections:
            config_data += templates.RPC

        # programs
        programs = [p for p in self.options.get('programs', '').splitlines()
                    if p]
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

        if "services" in self._sections:
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

                tpl_parameters = dict(
                    program=parts.get('processname'),
                    command=parts.get('command'),
                    priority=parts.get('priority'),
                    redirect_stderr=parts.get('redirect') or 'false',
                    directory=(parts.get('directory') or
                               os.path.dirname(parts.get('command'))),
                    args=parts.get('args') or '',
                    extra_config="\n".join(extras),
                )
                config_data += templates.PROGRAM % tpl_parameters

            # eventlisteners
            pattern = re.compile("(?P<processname>[^\s]+)"
                                 "(\s+\((?P<processopts>([^\)]+))\))?"
                                 "\s+"
                                 "(?P<events>[^\s]+)"
                                 "\s+"
                                 "(?P<command>[^\s]+)"
                                 "(\s+\[(?P<args>[^\]]+)\])?")

            ev_lines = self.options.get('eventlisteners', '').splitlines()
            eventlisteners = [e for e in ev_lines if e]

            for eventlistener in eventlisteners:
                match = pattern.match(eventlistener)
                if not match:
                    raise ValueError(
                        "Event Listeners line incorrect: {0}".format(
                            eventlistener
                        )
                    )

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
                ev_params = dict(**param)
                ev_params['name'] = parts.get('processname')
                ev_params['events'] = parts.get('events')
                ev_params['command'] = parts.get('command')
                ev_params['args'] = parts.get('args')
                ev_params['extra_config'] = "\n".join(extras)

                config_data += templates.EVENTLISTENER % ev_params

            # groups
            groups = [g for g in self.options.get('groups', '').splitlines()
                      if g]

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

                tpl_parameters = dict(
                    priority=parts.get('priority'),
                    group=parts.get('group'),
                    programs=parts.get('programs'),
                )
                config_data += templates.GROUP % tpl_parameters

            # include
            files = [f for f in self.options.get('include', '').splitlines()
                     if f]
            if files:
                stringfiles = " ".join(files)
                config_data += templates.INCLUDE % {'stringfiles': stringfiles}

        conf_file = self.options.get('supervisord-conf')

        if not os.path.exists(os.path.dirname(conf_file)):
            os.makedirs(os.path.dirname(conf_file))

        with open(conf_file, 'w') as cf:
            cf.write(config_data)

        return self._install_scripts()

    def _install_scripts(self):
        installed = []
        conf_file = self.options.get('supervisord-conf')

        init_stmt = 'import sys; sys.argv.extend(["-c","{0}"])'.format(
            conf_file
        )
        if 'global' in self._sections:
            dscript = zc.recipe.egg.Egg(
                self.buildout,
                self.name,
                {'eggs': 'supervisor',
                 'scripts': 'supervisord=%sd' % self.name,
                 'initialization': init_stmt,
                 })
            installed = list(dscript.install())

        memscript = zc.recipe.egg.Egg(
            self.buildout,
            self.name,
            {'eggs': 'supervisor',
             'scripts': 'memmon=memmon',
             })
        installed += list(memscript.install())

        init_stmt = 'import sys; sys.argv[1:1] = ["-c", "[0]"]'.format(
            conf_file
        )
        if 'ctl' in self._sections:
            ctlscript = zc.recipe.egg.Egg(
                self.buildout,
                self.name,
                {'eggs': 'supervisor',
                 'scripts': 'supervisorctl=%sctl' % self.name,
                 'initialization': init_stmt,
                 'arguments': 'sys.argv[1:]',
                 })
            installed += list(ctlscript.install())

        #install extra eggs if any
        plugins = self.options.get('plugins', '')
        if plugins:
            pluginsscript = zc.recipe.egg.Egg(
                self.buildout,
                self.name,
                {'eggs': plugins}
            )
            installed += list(pluginsscript.install())

        installed += [conf_file]
        return installed

    def update(self):
        """Updater"""
        return self._install_scripts()
