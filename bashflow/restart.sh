#!/bin/bash

cd database

docker compose down

sudo rm -r postgresql

cd ..

rm ./script/sql/schema.sql

touch ./script/sql/schema.sql

rm ./in/yellow_trips_2018-01.parquet

rm ./out/calendar.csv
rm ./out/borough.csv
rm ./out/condition.csv
rm ./out/icon.csv
rm ./out/location.csv
rm ./out/payment.csv
rm ./out/ratecode.csv
rm ./out/taxi_trips.csv
rm ./out/vendor.csv
rm ./out/weather.csv