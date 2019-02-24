FROM python:3.7.2

COPY . /app

WORKDIR /app

# Install modules required by our flask app (from requirements.txt)
#  and modules required by our deployment method (from requirements-in-container.txt).
#
RUN pip install -r requirements.txt  &&  pip install -r requirements-in-container.txt

EXPOSE 8000

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
CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "query-files-app:app"]