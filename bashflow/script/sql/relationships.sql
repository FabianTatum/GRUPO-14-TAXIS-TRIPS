-- Primary keys weather relations
ALTER TABLE "icon" ADD PRIMARY KEY ("IdIcon");
ALTER TABLE "condition" ADD PRIMARY KEY ("IdCondition");

-- Relaciones * weather -> condition
ALTER TABLE "weather"
ADD CONSTRAINT "weather_condition_fk"
FOREIGN KEY ("IdCondition") 
REFERENCES "condition"("IdCondition");

-- Relaciones * weather -> icon
ALTER TABLE "weather"
ADD CONSTRAINT "weather_icon_fk"
FOREIGN KEY ("IdIcon") 
REFERENCES "icon"("IdIcon");

-- Primary keys Trips
ALTER TABLE "taxi_trips" ADD PRIMARY KEY ("IdTaxis");
ALTER TABLE "vendor" ADD PRIMARY KEY ("IdVendor");
ALTER TABLE "ratecode" ADD PRIMARY KEY ("IdRatecode");
ALTER TABLE "payment" ADD PRIMARY KEY ("IdPayment_type");
ALTER TABLE "location" ADD PRIMARY KEY ("IdLocation");
ALTER TABLE "borough" ADD PRIMARY KEY ("IdBorough");

-- Relaciones * trips -> vendor
ALTER TABLE "taxi_trips"
ADD CONSTRAINT "taxitrips_vendor_fk"
FOREIGN KEY ("IdVendor") 
REFERENCES "vendor"("IdVendor");

-- Relaciones * trips -> ratecode
ALTER TABLE "taxi_trips"
ADD CONSTRAINT "taxitrips_ratecode_fk"
FOREIGN KEY ("IdRatecode") 
REFERENCES "ratecode"("IdRatecode");

-- Relaciones * trips -> payment
ALTER TABLE "taxi_trips"
ADD CONSTRAINT "taxitrips_payment_fk"
FOREIGN KEY ("IdPayment_type") 
REFERENCES "payment"("IdPayment_type");

-- Relaciones * Location -> Borough
ALTER TABLE "location"
ADD CONSTRAINT "location_borough_fk"
FOREIGN KEY ("IdBorough") 
REFERENCES "borough"("IdBorough");

-- Relaciones * trips -> PULocation -> location 
ALTER TABLE "taxi_trips"
ADD CONSTRAINT "taxitrips_IdPULocation_fk"
FOREIGN KEY ("IdPULocation") 
REFERENCES "location"("IdLocation");

\d weather
\d taxi_trips