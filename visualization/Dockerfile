#FROM python:3.8
FROM tiangolo/uwsgi-nginx-flask:python3.8
#RUN apt-get update
 
#RUN mkdir wd
#WORKDIR wd

#COPY app/requirements.txt .
#COPY app/test_requirements.txt .
COPY test_requirements.txt /tmp/

#COPY app/ ./
COPY ./app /app
#RUN pip3 install -r requirements.txt
RUN pip3 install -r /tmp/test_requirements.txt

# ENV LISTEN_PORT=5000
#EXPOSE 80
  
#CMD [ "python3", "-u", "app.py"]
#CMD [ "gunicorn", "--workers=5", "--threads=1", "-b 0.0.0.0:80", "app:server"]
ENV NGINX_WORKER_PROCESSES auto
ENV KAFKA_BROKER_URL=broker:29092
ENV LISTEN_TO_TOPICS=icesheets
ENV LISTENER_TIMEOUT=6000
#CMD [ "gunicorn", "--workers=5", "--threads=1", "-b 0.0.0.0:80", "mock_app:server"]
