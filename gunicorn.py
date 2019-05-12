import multiprocessing

chdir = '~/bus_py/'
bind = "0.0.0.0:8008"
worker_class = 'gevent'
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
reload = True
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
accesslog = "~/bus_py/logs/gunicorn_access.log"
loglevel = 'warning'  # 错误日志等级
errorlog = "~/bus_py/logs/gunicorn_error.log"
