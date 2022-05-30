FROM python:3.8
RUN apt-get update
 
RUN mkdir wd
WORKDIR wd
COPY app/requirements.txt .

RUN pip3 install -r requirements.txt

COPY app/ ./
  
#CMD [ "python3", "-u", "dash_stream.py"]
CMD [ "python3", "-u", "-b 0.0.0.0:80", "app:server"]
#CMD [ "gunicorn", "--workers=5", "--threads=1", "-b 0.0.0.0:80", "app:server"]
