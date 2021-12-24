USE 94_assign2db;
CREATE VIEW P4Q1 AS SELECT firstname, lastname, tripname, country, money FROM passenger, bustrip, book WHERE passenger.passengerid = book.passengerid AND bustrip.tripid = book.tripid;
SELECT * FROM P4Q1;
SELECT * FROM P4Q1 WHERE tripname LIKE '%Castles%' ORDER BY money;
SELECT * FROM bus;
DELETE FROM bus WHERE licenseplate LIKE '%UWO%';
SELECT * FROM bus;
SELECT * FROM passport;
SELECT * FROM passenger;
DELETE FROM passport WHERE citizenship ='Canada';
SELECT * FROM passport;
SELECT * FROM passenger;
-- ---------
-- The two table no longer have the same row because when you delete a passport, corresponding passenger won't get deleted due to the fact that when we initializing the table we didn't put ON DELETE CASCADE into the passenger table, but we put it into the passport table instead. So if you trying to delete a passenger the corresponding passport will be deleted.
SELECT * FROM bustrip;
DELETE FROM bustrip WHERE tripname = 'California Wines';
SELECT * FROM bustrip;
-- ---------
-- The data cannot be deleted because we added a constraint earlier indicating the bustrip and book are cascade.
DELETE FROM bustrip WHERE tripname = 'Arrivaderci Roma';
SELECT * FROM passenger;
DELETE FROM passenger WHERE firstname = 'Pam';
SELECT * FROM passenger;
SELECT * FROM P4Q1;
DELETE FROM passenger WHERE lastname = 'Simpson';
SELECT * FROM P4Q1;
