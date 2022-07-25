
CREATE TABLE "weather" (
"datetime" TIMESTAMP,
  "temp" TEXT,
  "feelslike" TEXT,
  "humidity" TEXT,
  "precip" TEXT,
  "snow" TEXT,
  "windspeed" TEXT,
  "IdCondition" INTEGER,
  "IdIcon" INTEGER
)
;
CREATE TABLE "icon" (
"state" TEXT,
  "IdIcon" INTEGER
)
;
CREATE TABLE "condition" (
"condition" TEXT,
  "IdCondition" INTEGER
)
;
CREATE TABLE "borough" (
"IdBorough" INTEGER,
  "Borough" TEXT,
  "Latitude" REAL,
  "Longitude" REAL
);

CREATE TABLE "location" (
"IdLocation" INTEGER,
  "IdBorough" INTEGER,
  "Zone" TEXT
);

CREATE TABLE "ratecode" (
"IdRatecode" INTEGER,
  "Name_ratecode" TEXT
);

CREATE TABLE "payment" (
"IdPayment_type" INTEGER,
  "Payment_type" TEXT
);

CREATE TABLE "vendor" (
"IdVendor" INTEGER,
  "Name_vendor" TEXT
);

CREATE TABLE "taxi_trips" (
  "IdTaxis_2018" INTEGER,
  "IdVendor" INTEGER,
  "tpep_pickup_datetime" TIMESTAMP,
  "tpep_dropoff_datetime" TIMESTAMP,
  "Travel_time" TEXT,
  "IdRatecode" INTEGER,
  "IdPULocation" INTEGER,
  "IdDOLocation" INTEGER,
  "IdPayment_type" INTEGER,
  "IdBorough" INTEGER,
  "fare_amount" REAL,
  "extra" REAL,
  "mta_tax" REAL,
  "tip_amount" REAL,
  "improvement_surcharge" REAL,
  "total_amount_1" REAL
);

