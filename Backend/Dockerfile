FROM ubuntu:20.04

WORKDIR /app

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev && \
    apt-get install tesseract-ocr -y \
    build-essential libssl-dev libffi-dev python3-setuptools \
    python3-venv mongodb-clients

RUN pip install pillow
RUN pip install pytesseract
RUN pip install opencv-contrib-python

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0


COPY ./Backend/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 5000
#COPY . .

# CMD tail -f /dev/null
# CMD [ "python3", "app.py" ]
CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "app:app" ]