#!/bin/bash

echo
echo "------------------------- Iniciando configuraçao de virtualenv -------------------------"
echo

python3 -m pip install --upgrade pip
pip3 install virtualenv
virtualenv venv/market_place -p python3
source venv/market_place/bin/activate
cd MarketPlace_api/
pip3 install -r requirements.txt

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
python3 manage.py migrate
python3 manage.py runserver