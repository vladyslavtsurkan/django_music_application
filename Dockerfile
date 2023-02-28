FROM python:3.11.2

WORKDIR /music_application

COPY requirements.txt /music_application

RUN pip install -r requirements.txt

COPY . .
