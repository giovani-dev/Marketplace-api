FROM python:3.8
ENV PYTHONUNBUFFERED=1

RUN mkdir /api
WORKDIR /api

ADD . /api/

COPY requirements.txt /api/

RUN pip install -r requirements.txt

EXPOSE 8000
CMD gunicorn MarketPlace.wsgi:application --bind 0.0.0.0:8000