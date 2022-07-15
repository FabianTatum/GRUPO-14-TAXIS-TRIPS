#!/bin/bash

export PG_HOST=127.0.0.1
export PG_USER=root
export PG_PASSWORD=root
export PGPASSWORD="$PG_PASSWORD"
export PG_PORT=5432
export PG_DATABASE=ny_taxi

### Descarga de datos de yellow_trips
curl -o ./in/yellow_trips_2018-01.parquet https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2018-01.parquet

### Descarga de los datos de tiempo
python3 ./script/python/extract.py

### Transformacion de datos
echo "Please Wait..."
sleep 5 

python3 ./script/python/transform.py

# Levantar container
cd database

docker compose up -d
echo "Please wait 10 seconds..."
sleep 10

cd ..

### carga a postgres

echo "Creando tablas.."
### Creacion de las tablas a ingestar
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DATABASE -f ./script/sql/schema.sql 
echo "Tablas creadas."

MYHOME=$(pwd)

echo "Ingestando datos..."
echo "---------------------------------------"

echo "Datos de calendario"
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DATABASE -c "\copy PUBLIC.calendar FROM \
'$MYHOME/out/calendar.csv' DELIMITER ',' CSV HEADER;"

echo "Datos de condition"
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DATABASE -c "\copy PUBLIC.condition FROM \
'$MYHOME/out/condition.csv' DELIMITER ',' CSV HEADER;"

echo "Datos de icon"
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DATABASE -c "\copy PUBLIC.icon FROM \
'$MYHOME/out/icon.csv' DELIMITER ',' CSV HEADER;"

echo "Datos de location"
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DATABASE -c "\copy PUBLIC.location FROM \
'$MYHOME/out/location.csv' DELIMITER ',' CSV HEADER;"

echo "Datos de payment"
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DATABASE -c "\copy PUBLIC.payment FROM \
'$MYHOME/out/payment.csv' DELIMITER ',' CSV HEADER;"

echo "Datos de ratecode"
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DATABASE -c "\copy PUBLIC.ratecode FROM \
'$MYHOME/out/ratecode.csv' DELIMITER ',' CSV HEADER;"

echo "Datos de taxi_trips"
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DATABASE -c "\copy PUBLIC.taxi_trips FROM \
'$MYHOME/out/taxi_trips.csv' DELIMITER ',' CSV HEADER;"

echo "Datos de vendor"
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DATABASE -c "\copy PUBLIC.vendor FROM \
'$MYHOME/out/vendor.csv' DELIMITER ',' CSV HEADER;"

echo "Datos de weather"
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DATABASE -c "\copy PUBLIC.weather FROM \
'$MYHOME/out/weather.csv' DELIMITER ',' CSV HEADER;"

echo "Ver las tablas..."
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DATABASE -c "\dt"

echo "-----------------------------------------"
echo "||||   CREACION DE LAS RELACIONES    ||||"
echo "-----------------------------------------"

#psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DATABASE -f ./script/sql/relationships.sql