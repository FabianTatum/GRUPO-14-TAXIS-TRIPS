-- Primary keys weather relations
ALTER TABLE "icon" ADD PRIMARY KEY ("idicon");
ALTER TABLE "condition" ADD PRIMARY KEY ("idcondition");

-- Relaciones * weather -> condition
ALTER TABLE "weather"
ADD CONSTRAINT "weather_condition_fk"
FOREIGN KEY ("idcondition") 
REFERENCES "condition"("idcondition");

-- Relaciones * weather -> icon
ALTER TABLE "weather"
ADD CONSTRAINT "weather_icon_fk"
FOREIGN KEY ("idicon") 
REFERENCES "icon"("idicon");

-- Primary keys Trips
ALTER TABLE "vendor" ADD PRIMARY KEY ("idvendor");
ALTER TABLE "ratecode" ADD PRIMARY KEY ("idratecode");
ALTER TABLE "payment" ADD PRIMARY KEY ("idpayment_type");
ALTER TABLE "location" ADD PRIMARY KEY ("idlocation");
ALTER TABLE "borough" ADD PRIMARY KEY ("idborough");

-- Relaciones * trips -> vendor
ALTER TABLE "taxi_trips"
ADD CONSTRAINT "taxitrips_vendor_fk"
FOREIGN KEY ("idvendor") 
REFERENCES "vendor"("idvendor");

-- Relaciones * trips -> ratecode
ALTER TABLE "taxi_trips"
ADD CONSTRAINT "taxitrips_ratecode_fk"
FOREIGN KEY ("idratecode") 
REFERENCES "ratecode"("idratecode");

-- Relaciones * trips -> payment
ALTER TABLE "taxi_trips"
ADD CONSTRAINT "taxitrips_payment_fk"
FOREIGN KEY ("idpayment_type") 
REFERENCES "payment"("idpayment_type");

-- Relaciones * Location -> Borough
ALTER TABLE "location"
ADD CONSTRAINT "location_borough_fk"
FOREIGN KEY ("idborough") 
REFERENCES "borough"("idborough");

-- Relaciones * trips -> PULocation -> location 
ALTER TABLE "taxi_trips"
ADD CONSTRAINT "taxitrips_IdPULocation_fk"
FOREIGN KEY ("IdPULocation") 
REFERENCES "location"("idlocation");
