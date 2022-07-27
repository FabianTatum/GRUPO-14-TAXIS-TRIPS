#!/bin/bash

#############################
#--- ENV POSTGRES HEROKU ---#
#############################
#export PG_HOST=ec2-54-152-28-9.compute-1.amazonaws.com
#export PG_USER=rrjwtvrnfmwzdq
#export PG_PASSWORD=ec84e8311185382386aeb980fdccd0cb25419e6896b867cdc5646673495f0d5e
#export PG_PORT=5432
#export PG_DATABASE=d87pqc6aa32el4

#export PGPASSWORD="$PG_PASSWORD"

while getopts f:h: flag
do
    case "${flag}" in
        f) fecha=${OPTARG};;
        h) how=${OPTARG};;
    esac
done
echo "Fecha Escogida: $fecha";
echo "Tipo de carga: $how";

charge='yes'

#############################
#--- ENV POSTGRES DOCKER ---#
#############################
export PG_HOST=127.0.0.1
export PG_USER=root
export PG_PASSWORD=root
export PG_PORT=5432
export PG_DATABASE=ny_taxi

export PGPASSWORD="$PG_PASSWORD"


while [[ $charge == 'yes' ]]
do
    ### Descarga de datos de yellow_trips
    echo -e "\n----------------------------------------"
    echo "----------------------------------------"
    echo "         EXTRACT PHASE INITIALIZED      "
    echo "----------------------------------------"
    echo -e "----------------------------------------\n"

    echo -e "[$(date +"%Y-%m-%d - %T")] - Extract Data from TLC New York initialized.\n"
    curl -o ./in/yellow_trips_$fecha.parquet https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_$fecha.parquet
    echo -e "[$(date +"%Y-%m-%d - %T")] - Extract Data from TLC New York successfuly.\n"

    ### Descarga de los datos de tiempo
    echo "[$(date +"%Y-%m-%d - %T")] - Extract Data from Weather New York Zone initialized"
    python3 ./script/python/extract.py  # TODO: Debo pasarle la fecha del mes
    echo "[$(date +"%Y-%m-%d - %T")] - Extract Data from Weather New York Zone successfuly"

    echo -e "\n **** EXTRACTED PHASE SUCCESSFULY ******* \n"

    echo -e "\n Please Wait... \n"

    echo -e "\n----------------------------------------"
    echo  "----------------------------------------"
    echo  "         TRANSFORM PHASE INITIALIZED    "
    echo  "----------------------------------------"
    echo -e "----------------------------------------\n"

    echo -e "[$(date +"%Y-%m-%d - %T")] - Transform Data from TLC New York initialized. \n"
    python3 ./script/python/load.py $fecha
    echo -e "\n[$(date +"%Y-%m-%d - %T")] - Transform Data from TLC New York successfuly"

    echo -e "\n ********* TRANSFORM PHASE SUCCESSFULY *********** \n"

    echo -e "\n Please Wait... \n"

    if [[ $how == initial ]]
    then

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
        echo "[$(date +"%Y-%m-%d - %T")] - Docker container PostgreSQL and PgAdmin successs."
        cd ..

        sleep 15

        echo -e "\n Please Wait... \n"

    fi

    echo  -e "\n----------------------------------------"
    echo  "----------------------------------------"
    echo  "          LOAD PHASE INITIALIZED        "
    echo  "----------------------------------------"
    echo  -e "------------------------------------------\n"

    if [[ $how == initial ]]
    then

        echo -e "[$(date +"%Y-%m-%d - %T")] - Create tables initialized. \n"
        ### Creacion de las tablas a ingestar
        psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DATABASE -f ./script/sql/schema.sql 
        echo -e "[$(date +"%Y-%m-%d - %T")] - Create tables successfuly.\n"
    
    fi

    MYHOME=$(pwd)

    echo -e "[$(date +"%Y-%m-%d - %T")] - LOAD DATA IN DATAWAREHOUSE INITIALIZED.\n"

    if [[ $how == initial ]]
    then

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

        echo "[$(date +"%Y-%m-%d - %T")] - Load data vendor."
        psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DATABASE -c "\copy PUBLIC.vendor FROM \
        '$MYHOME/out/vendor.csv' DELIMITER ',' CSV HEADER;"

        echo "[$(date +"%Y-%m-%d - %T")] - Load data weather."
        psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DATABASE -c "\copy PUBLIC.weather FROM \
        '$MYHOME/out/weather.csv' DELIMITER ',' CSV HEADER;"
    fi

    echo "[$(date +"%Y-%m-%d - %T")] - Load data trips."
    psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DATABASE -c "\copy PUBLIC.taxi_trips FROM \
    '$MYHOME/out/taxi_trips.csv' DELIMITER ',' CSV HEADER;"


    echo "[$(date +"%Y-%m-%d - %T")] - View Tables."
    psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DATABASE -c "\dt"

    echo -e "\n********* LOAD PHASE SUCCESSFULY **********\n"

    echo -e "\n Please Wait... \n"

    if [[ $how == initial ]]
    then

        echo -e "\n--------- CREATE RELATIONSHIPS BETWEEN TABLES ----------\n"

        echo "[$(date +"%Y-%m-%d - %T")] - Create relationships initialized."
        echo -e "\n----------- SHOW RELATIONSHIPS IN DATA WAREHOUSE -------------\n" 
        psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DATABASE -f ./script/sql/relationships.sql
        echo "[$(date +"%Y-%m-%d - %T")] - Create relationships successfuly."

        echo -e "\n Please Wait... \n"
    
    fi

    echo "Desea realizar otra carga [yes/no]:"
    read input

    charge=$input

    if [[ $charge != 'yes' ]]
    then
        echo " -- Proceso finalizado -- "
        break
    fi

    echo "Fecha de la carga [AÑO-MES]:"
    read new_fecha
    fecha=$new_fecha
    how=incremental

done