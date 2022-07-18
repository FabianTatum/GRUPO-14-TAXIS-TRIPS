#!/bin/bash

export PG_HOST=127.0.0.1
export PG_USER=root
export PG_PASSWORD=root
export PGPASSWORD="$PG_PASSWORD"
export PG_PORT=5432
export PG_DATABASE=ny_taxi

### Descarga de datos de yellow_trips

echo -e "\n----------------------------------------"
echo "----------------------------------------"
echo "         EXTRACT PHASE INITIALIZED      "
echo "----------------------------------------"
echo -e "----------------------------------------\n"

echo -e "[$(date +"%Y-%m-%d - %T")] - Extract Data from TLC New York initialized.\n"
curl -o ./in/yellow_trips_2018-01.parquet https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2018-01.parquet
echo -e "[$(date +"%Y-%m-%d - %T")] - Extract Data from TLC New York successfuly.\n"

### Descarga de los datos de tiempo
echo "[$(date +"%Y-%m-%d - %T")] - Extract Data from Weather New York Zone initialized"
python3 ./script/python/extract.py
echo "[$(date +"%Y-%m-%d - %T")] - Extract Data from Weather New York Zone successfuly"

echo -e "\n **** EXTRACTED PHASE SUCCESSFULY ******* \n"

echo -e "\n Please Wait... \n"
sleep 20 

echo -e "\n----------------------------------------"
echo  "----------------------------------------"
echo  "         TRANSFORM PHASE INITIALIZED    "
echo  "----------------------------------------"
echo -e "----------------------------------------\n"

echo -e "[$(date +"%Y-%m-%d - %T")] - Transform Data from TLC New York initialized. \n"
python3 ./script/python/transform.py
echo -e "\n[$(date +"%Y-%m-%d - %T")] - Transform Data from TLC New York successfuly"

echo -e "\n ********* TRANSFORM PHASE SUCCESSFULY *********** \n"

echo -e "\n Please Wait... \n"
sleep 10 


echo -e "\n----------------------------------------"
echo  "----------------------------------------"
echo  "     DOCKER POSTGRES DATA WAREHOUSE     "
echo  "----------------------------------------"
echo -e "------------------------------------------\n"

# Levantar container
cd database

echo "[$(date +"%Y-%m-%d - %T")] - Docker container PostgreSQL and PgAdmin initialized."
docker compose up -d
echo -e "\nPlease wait few seconds...\n"
sleep 10
echo "[$(date +"%Y-%m-%d - %T")] - Docker container PostgreSQL and PgAdmin successs."

echo -e "\n Please Wait... \n"
sleep 10 

echo  -e "\n----------------------------------------"
echo  "----------------------------------------"
echo  "          LOAD PHASE INITIALIZED        "
echo  "----------------------------------------"
echo  -e "------------------------------------------\n"

cd ..

echo -e "[$(date +"%Y-%m-%d - %T")] - Create tables initialized. \n"
### Creacion de las tablas a ingestar
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DATABASE -f ./script/sql/schema.sql 
echo "[$(date +"%Y-%m-%d - %T")] - Create tables successfuly.\n"

sleep 10

MYHOME=$(pwd)

echo "[$(date +"%Y-%m-%d - %T")] - LOAD DATA IN DATAWAREHOUSE INITIALIZED.\n"

echo "[$(date +"%Y-%m-%d - %T")] - Load data calendar."
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DATABASE -c "\copy PUBLIC.calendar FROM \
'$MYHOME/out/calendar.csv' DELIMITER ',' CSV HEADER;"

echo "[$(date +"%Y-%m-%d - %T")] - Load data condition."
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DATABASE -c "\copy PUBLIC.condition FROM \
'$MYHOME/out/condition.csv' DELIMITER ',' CSV HEADER;"

echo "[$(date +"%Y-%m-%d - %T")] - Load data icon."
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DATABASE -c "\copy PUBLIC.icon FROM \
'$MYHOME/out/icon.csv' DELIMITER ',' CSV HEADER;"

echo "[$(date +"%Y-%m-%d - %T")] - Load data borough."
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DATABASE -c "\copy PUBLIC.borough FROM \
'$MYHOME/out/borough.csv' DELIMITER ',' CSV HEADER;"

echo "[$(date +"%Y-%m-%d - %T")] - Load data location."
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DATABASE -c "\copy PUBLIC.location FROM \
'$MYHOME/out/location.csv' DELIMITER ',' CSV HEADER;"

echo "[$(date +"%Y-%m-%d - %T")] - Load data payment."
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DATABASE -c "\copy PUBLIC.payment FROM \
'$MYHOME/out/payment.csv' DELIMITER ',' CSV HEADER;"

echo "[$(date +"%Y-%m-%d - %T")] - Load data ratecode."
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DATABASE -c "\copy PUBLIC.ratecode FROM \
'$MYHOME/out/ratecode.csv' DELIMITER ',' CSV HEADER;"

echo "[$(date +"%Y-%m-%d - %T")] - Load data trips."
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DATABASE -c "\copy PUBLIC.taxi_trips FROM \
'$MYHOME/out/taxi_trips.csv' DELIMITER ',' CSV HEADER;"

echo "[$(date +"%Y-%m-%d - %T")] - Load data vendor."
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DATABASE -c "\copy PUBLIC.vendor FROM \
'$MYHOME/out/vendor.csv' DELIMITER ',' CSV HEADER;"

echo "[$(date +"%Y-%m-%d - %T")] - Load data weather."
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DATABASE -c "\copy PUBLIC.weather FROM \
'$MYHOME/out/weather.csv' DELIMITER ',' CSV HEADER;"

echo "[$(date +"%Y-%m-%d - %T")] - Load data weather."
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DATABASE -c "\dt"

echo -e "\n********* LOAD PHASE SUCCESSFULY **********\n"

echo -e "\n Please Wait... \n"
sleep 10 

echo -e "\n--------- CREATE RELATIONSHIPS BETWEEN TABLES ----------\n"

echo "[$(date +"%Y-%m-%d - %T")] - Create relationships initialized."
echo -e "\n----------- SHOW RELATIONSHIPS IN DATA WAREHOUSE -------------\n" 
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DATABASE -f ./script/sql/relationships.sql
echo "[$(date +"%Y-%m-%d - %T")] - Create relationships successfuly."

echo -e "\n Please Wait... \n"
sleep 10 

more contributors.txt
