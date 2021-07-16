FROM ubuntu:20.04

WORKDIR /app
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update && apt-get -y install libgl1-mesa-glx && \
    apt-get -y install libtesseract-dev &&\
    apt-get -y install tesseract-ocr && \
    apt-get install -y python3-pip python3-dev \
    build-essential libssl-dev libffi-dev python3-setuptools \
    python3-venv mongodb-clients


# RUN apt-get -y install tesseract-ocr 


# RUN apt-get -y install libgl1-mesa-glx
# RUN apt-get -y install libtesseract-dev

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0


COPY ./Backend/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 5000
#COPY . .

# CMD tail -f /dev/null
# CMD [ "python3", "app.py" ]
CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "app:app" ]