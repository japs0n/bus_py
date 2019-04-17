import multiprocessing

chdir = '/home/ubuntu/Yijiandianzao'
bind = "127.0.0.1:5000"
worker_class = 'gevent'
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
reload = True
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
accesslog = "/home/ubuntu/Yijiandianzao/logs/gunicorn_access.log"
loglevel = 'info'  # 错误日志等级
errorlog = "/home/ubuntu/Yijiandianzao/logs/gunicorn_error.log"
