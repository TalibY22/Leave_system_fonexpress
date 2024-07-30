bind = '192.168.0.38:8000'
workers = 3
timeout = 120


#number of workers = 2 * number of CPU cores + 1
#cd\
#gunicorn -c gunicorn.py Leave_system_fonexpress.wsgi:application

worker_class = 'gevent'
worker_connections = 1000