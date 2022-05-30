FROM python:3.8
RUN apt-get update
 
RUN mkdir wd
WORKDIR wd
COPY app/requirements.txt .

RUN pip3 install -r requirements.txt

COPY app/ ./
# ENV LISTEN_PORT=5000
# EXPOSE 5000
  
#CMD [ "python3", "-u", "app.py"]
CMD [ "gunicorn", "--workers=5", "--threads=1", "-b 0.0.0.0:80", "app:server"]
