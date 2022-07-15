ALTER TABLE "icon" ADD PRIMARY KEY ("IdIcon");
\d icon
ALTER TABLE "condition" ADD PRIMARY KEY ("IdCondition");
\d condition

--ALTER TABLE table_name ADD COLUMN column_name DATATYPE 
--REFERENCES referenced_table_name(referenced_column_name);

ALTER TABLE weather ADD COLUMN IdCondition INTEGER REFERENCES condition(IdCondition);
ALTER TABLE weather ADD COLUMN IdIcon INTEGER REFERENCES icon(IdIcon);
\d weather
