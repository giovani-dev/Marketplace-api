FROM python:3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /src/MarketPlace
COPY requirements.txt /src/MarketPlace/
RUN pip install -r requirements.txt
COPY . /src/MarketPlace/