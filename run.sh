cd MarketPlace/
docker build -t api_market_place .
cd ../
docker-compose build

docker run api_market_place -d
docker-compose up -d

echo 
echo "====================================="
echo "PROJETO INICIADO COM SUCESSO!"
echo "====================================="
echo