# Gunicorn Configuration File for craftdot frontendls 

# Number of worker processes for handling requests
# Adjust this number based on the available CPU cores on your server
workers = 2

# The type of worker processes to use
# 'sync' is the default worker class, which is suitable for most web applications
# Other options include 'gevent', 'eventlet', and 'tornado' for asynchronous workers
worker_class = 'sync'

# Address and port to bind the server to
# You can specify a specific IP address (e.g., '127.0.0.1:8000') or bind to all interfaces ('0.0.0.0:8000')
bind = '127.0.0.1:8001'

# Log levels: 'debug', 'info', 'warning', 'error', 'critical'
loglevel = 'info'

# Directory to store the PID file
# This file keeps track of the Gunicorn process ID (PID)
pidfile = '/var/run/gunicorn/craftdot_frontend_gunicorn.pid'

# Directory to store access logs
# Access logs contain information about each HTTP request
accesslog = '/var/log/gunicorn/craftdot_frontend_access.log'

# Directory to store error logs
# Error logs contain information about errors that occur during request handling
errorlog = '/var/log/gunicorn/craftdot_frontend_error.log'

# Timeout in seconds for requests
# If a worker does not respond to a request within this time, Gunicorn will terminate the worker
timeout = 30

# ###Number of seconds to wait before restarting a worker after a crash
graceful_timeout = 10

# Reload when codebase change
reload = True
