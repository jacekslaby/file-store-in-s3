FROM python:3.7.2

COPY requirements-in-container.txt /app/

WORKDIR /app

# Install modules required by our flask app (BUT not from requirements.txt, which contains too much, e.g. test libs)
#  and modules required by our deployment method.
#
RUN pip install -r requirements-in-container.txt

# WSGI HTTP Server will be exposed on this port.
EXPOSE 8000

# Copy our application code.
# (Note: We use 'COPY .' because we need to copy files _including_ their folders.
#   We use file .dockerignore in order to avoid unwanted files, e.g. virtualenv stack and tests.)
#
COPY . /app

# Run WSGI HTTP Server serving our app.
#
# (references:
#  http://docs.gunicorn.org/en/stable/run.html
#  https://nickjanetakis.com/blog/dockerize-a-flask-celery-and-redis-application-with-docker-compose
#  https://stackoverflow.com/questions/43925487/how-to-run-gunicorn-on-docker
#  https://www.fullstackpython.com/docker.html
# 
# @TODO Add user.   ("it is not a good practice to run an application as root" - https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xix-deployment-on-docker-containers )
# @TODO Add nginx.  (as in "Deploying Gunicorn - We strongly recommend to use Gunicorn behind a proxy server.")
#
CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "--access-logfile=-", "--log-level=info", "queryfilesapp:app"]