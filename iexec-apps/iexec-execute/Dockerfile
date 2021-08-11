FROM python:3.7.3-alpine3.10

### install python3 dependencies you need
RUN pip install --upgrade pip
RUN pip3 install wget

COPY ./src /app

###  protect file system with Scone
#COPY ./protect-fs.sh ./Dockerfile /build/
#RUN sh /build/protect-fs.sh /app

ENTRYPOINT ["python", "/app/app.py"]