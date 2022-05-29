FROM python:3.8-slim-buster
RUN apt-get update
RUN apt-get install nano
 
RUN mkdir wd
WORKDIR wd
COPY app/requirements.txt .
RUN pip3 install -r requirements.txt
  
COPY app/ ./
  
CMD [ "gunicorn", "--workers=5", "--threads=1", "-b 127.0.0.1:9042", "app:server"]