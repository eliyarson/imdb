# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.7


ENV GROUP_ID=1000 \
    USER_ID=1000

# Install manually all the missing libraries
RUN apt-get update

# Install Python dependencies.
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy local code to the container image.
ENV APP_HOME /var/www/
WORKDIR $APP_HOME
COPY . .

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
RUN addgroup -gid ${GROUP_ID} www
RUN adduser --disabled-password -u ${USER_ID} www --ingroup www --shell /bin/sh

USER www

EXPOSE 5000

CMD exec gunicorn --bind :5000 --workers 4 --threads 8 wsgi:application --reload
