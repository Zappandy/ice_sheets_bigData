FROM python:3.8-slim-buster
RUN apt-get update
RUN apt-get install nano
 
RUN mkdir wd
WORKDIR wd
COPY visualization/requirements.txt .
RUN pip3 install -r requirements.txt
  
COPY visualization/ ./
  
CMD [ "gunicorn", "--workers=5", "--threads=1", "-b 0.0.0.0:80", "app:server"]