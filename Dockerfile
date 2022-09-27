FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir /first_project

WORKDIR /first_project

COPY requirements.txt /first_project/

RUN pip install --upgrade pip && pip install -r requirements.txt

ADD . /first_project/