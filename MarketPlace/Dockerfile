FROM python:3.8
ENV PYTHONUNBUFFERED=1

RUN mkdir /api
WORKDIR /api

ADD . /api/

COPY requirements.txt /api/

RUN pip install -r requirements.txt

# COPY entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh

EXPOSE 8000
# CMD python manage.py migrate
CMD gunicorn MarketPlace.wsgi:application --bind 0.0.0.0:8000
# CMD python manage.py migrate