GLOBAL = """\
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

PATH = """\
environment=PATH=%(env_path)s
"""

CTL = """\
[supervisorctl]
serverurl = %(serverurl)s
username = %(user)s
password = %(password)s

"""

INET_HTTP = """\
[inet_http_server]
port = %(port)s
username = %(user)s
password = %(password)s

"""

UNIX_HTTP = """\
[unix_http_server]
file = %(file)s
username = %(user)s
password = %(password)s
chmod = %(chmod)s
%(chown)s

"""

RPC = """\
[rpcinterface:supervisor]
supervisor.rpcinterface_factory=supervisor.rpcinterface:make_main_rpcinterface

"""

PROGRAM = """\
[program:%(program)s]
command = %(command)s %(args)s
process_name = %(program)s
directory = %(directory)s
priority = %(priority)s
redirect_stderr = %(redirect_stderr)s
%(extra_config)s
"""

EVENTLISTENER = """
[eventlistener:%(name)s]
command = %(command)s %(args)s
events = %(events)s
process_name=%(name)s
environment=SUPERVISOR_USERNAME='%(user)s',SUPERVISOR_PASSWORD='%(password)s',\
SUPERVISOR_SERVER_URL='%(serverurl)s'
%(extra_config)s
"""

GROUP = """
[group:%(group)s]
programs = %(programs)s
priority = %(priority)s
"""

INCLUDE = """
[include]
files = %(stringfiles)s
"""
