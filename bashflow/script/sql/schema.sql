
CREATE TABLE "weather" (
  "datetime" TIMESTAMP,
  "temp" TEXT,
  "feelslike" TEXT,
  "humidity" TEXT,
  "precip" TEXT,
  "snow" TEXT,
  "windspeed" TEXT,
  "idcondition" INTEGER,
  "idicon" INTEGER
)
;
CREATE TABLE "icon" (
  "state" TEXT,
  "idicon" INTEGER
)
;
CREATE TABLE "condition" (
"condition" TEXT,
  "idcondition" INTEGER
)
;
CREATE TABLE "borough" (
  "idborough" INTEGER,
  "borough" TEXT,
  "latitude" REAL,
  "longitude" REAL
);

CREATE TABLE "location" (
  "idlocation" INTEGER,
  "idborough" INTEGER,
  "Zone" TEXT
);

CREATE TABLE "ratecode" (
"idratecode" INTEGER,
  "name_ratecode" TEXT
);

CREATE TABLE "payment" (
  "idpayment_type" INTEGER,
  "payment_type" TEXT
);

CREATE TABLE "vendor" (
  "idvendor" INTEGER,
  "name_vendor" TEXT
);

CREATE TABLE "taxi_trips" (
  "idtaxis_2018" INTEGER,
  "idvendor" INTEGER,
  "tpep_pickup_datetime" TIMESTAMP,
  "tpep_dropoff_datetime" TIMESTAMP,
  "trip_distance" REAL,
  "travel_time" TEXT,
  "idratecode" INTEGER,
  "idpulocation" INTEGER,
  "iddolocation" INTEGER,
  "idpayment_type" INTEGER,
  "idborough" INTEGER,
  "idlocation" INTEGER,
  "fare_amount" REAL,
  "extra" REAL,
  "mta_tax" REAL,
  "tip_amount" REAL,
  "improvement_surcharge" REAL,
  "total_amount_1" REAL
);

