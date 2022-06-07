bind = "0.0.0.0:8000"
workers = 3
accesslog = "/dropform-backend/logs/gunicorn.access.log"
errorlog = "/dropform-backend/logs/gunicorn.app.log"
capture_output = True
loglevel = "info"
