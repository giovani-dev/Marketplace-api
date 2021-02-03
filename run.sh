#!/bin/bash

echo
echo "------------------------- Iniciando configuraçao de virtualenv -------------------------"
echo

python -m pip install --upgrade pip
pip install virtualenv
virtualenv venv/market_place -p python3.8
source venv/market_place/bin/activate
cd MarketPlace_api/
pip install -r requirements.txt

echo
echo "------------------------- Iniciando configuraçao do Docker -------------------------"
echo

cd ../
docker-compose down
docker-compose build
docker-compose up -d

echo
echo "------------------------- Iniciando projeto -------------------------"
echo

cd MarketPlace_api/
python manage.py migrate
python manage.py runserver