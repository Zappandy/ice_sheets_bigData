FROM python:3.8
RUN apt-get update
 
#RUN mkdir wd
#WORKDIR wd
#COPY app/requirements.txt .
COPY dash_stream.py ./
COPY requirements.txt ./
RUN chmod +x dash_stream.py
RUN chmod +x requirements.txt
RUN pip3 install -r requirements.txt

#COPY app/ ./
  
CMD [ "python3", "-u", "dash_stream.py"]
#CMD [ "gunicorn", "--workers=5", "--threads=1", "-b 0.0.0.0:80", "app:server"]
