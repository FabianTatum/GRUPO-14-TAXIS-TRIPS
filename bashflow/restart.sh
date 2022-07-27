#!/bin/bash

cd database

docker compose down

sudo rm -r postgresql

cd ..

rm ./in/yellow_trips_*.parquet

rm ./out/borough.csv
rm ./out/condition.csv
rm ./out/icon.csv
rm ./out/location.csv
rm ./out/payment.csv
rm ./out/ratecode.csv
rm ./out/taxi_trips.csv
rm ./out/vendor.csv
rm ./out/weather.csv