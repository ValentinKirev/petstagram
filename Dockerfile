FROM python:3.10

RUN apt update -y && apt upgrade -y

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV HOME=/home/app
ENV APP_HOME=/home/app/web

ENV STATICFILES_HOME=/staticfiles

RUN mkdir -p $STATICFILES_HOME

WORKDIR $APP_HOME

RUN pip install --upgrade pip

COPY . $APP_HOME

RUN pip install -r requirements.txt

