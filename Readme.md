* Overview: </br>
This project is based on two endpoints, one to send proposals for analysis and one to list based on consumer data
</br></br>

* Documentation: </br>
https://app.swaggerhub.com/apis/giovani-dev/Market_Place/1.0.0
</br></br>

* Obs.: </br>
Before you run the project, make sure if you are using Ubuntu or other SO distribuition based on linux kernel for use the run.sh, or make sure if your SO is able to use bash script 

</br></br>

* Run the script:
1. sh run.sh 
2. After you run the "run.sh", open a new terminal and activate you virtual enviroment and start celery. </br>
2.1 source venv/market_place/bin/activate </br>
2.2 celery -A MarketPlace worker -l info -B 
3. Please, run this project in python 3.8 for a better experience
