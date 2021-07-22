FROM ubuntu:20.04

WORKDIR /app


RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev \
    build-essential libssl-dev libffi-dev python3-setuptools \
    python3-venv mongodb-clients

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV DEBUG_METRICS = 1

COPY ./Backend/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

#relative with ImportError: libGL.so.1 
RUN apt-get -y install libgl1-mesa-glx 

RUN pip3 install imageai --upgrade
RUN pip3 install pytesseract

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get install tesseract-ocr-kor -y

EXPOSE 5000
EXPOSE 27017

# CMD tail -f /dev/null
# CMD [ "python3", "app.py" ]
CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "app:app" ]