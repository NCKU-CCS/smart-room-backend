# pylint: skip-file
bind = '0.0.0.0:5000'
workers = 4
timeout = 120
proc_name = 'SMART-ROOM-BACKEND'

errorlog = '-'
loglevel = 'info'
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
