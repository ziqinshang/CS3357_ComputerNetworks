USE 94_assign2db;
-- ---------
-- Query 1
SELECT tripname FROM bustrip WHERE country = 'Italy';
-- ---------
-- Query 2
SELECT DISTINCT lastname FROM passenger;
-- ---------
-- Query 3
SELECT * FROM bustrip ORDER BY tripname;
-- ---------
-- Query 4
SELECT tripname,country,startdate FROM bustrip WHERE startdate > '2022-04-30';
-- ---------
-- Query 5
SELECT firstname,lastname,birthdate FROM passenger,passport WHERE passenger.passengerid = passport.passengerid AND passport.citizenship = 'USA';
-- ---------
-- Query 6
SELECT tripname,capacity FROM bustrip,bus WHERE startdate >='2022-04-01' AND startdate<'2022-09-01' AND bustrip.licenseplate = bus.licenseplate;
-- ---------
-- Query 7
SELECT * FROM passenger,passport WHERE expirydate <= ADDDATE(CURDATE(),INTERVAL 1 YEAR) AND passenger.passengerid = passport.passengerid;
-- ---------
-- Query 8
SELECT firstname,lastname,tripname FROM passenger,bustrip,book WHERE passenger.passengerid = book.passengerid AND bustrip.tripid = book.tripid AND lastname LIKE "S%";
-- ---------
-- Query 9
SELECT COUNT(DISTINCT passengerid),tripname,bustrip.tripid FROM book,bustrip WHERE book.tripid = 1;
-- ---------
-- Query 10
SELECT country, SUM(Money) FROM bustrip,book WHERE bustrip.tripid = book.tripid GROUP BY country;
-- ---------
-- Query 11
SELECT firstname,lastname,citizenship,tripname,country FROM book,passenger,bustrip,passport WHERE passenger.passengerid = book.passengerid AND bustrip.tripid = book.tripid AND book.passengerid = passport.passengerid AND passport.citizenship != bustrip.country;
-- ---------
-- Query 12
SELECT DISTINCT bustrip.tripid,tripname FROM bustrip,book WHERE bustrip.tripid NOT IN (SELECT DISTINCT bustrip.tripid FROM bustrip,book WHERE bustrip.tripid = book.tripid);
-- ---------
-- Query 13
CREATE VIEW moneyspent AS SELECT firstname,lastname,citizenship,money FROM passenger, passport,book WHERE passenger.passengerid = passport.passengerid AND passenger.passengerid = book.passengerid;
SELECT firstname,lastname,citizenship,SUM(money) FROM moneyspent GROUP BY firstname,lastname ORDER BY SUM(money)desc;
-- ---------
-- Query 14
SELECT tripname FROM bustrip,book WHERE bustrip.tripid = book.tripid GROUP BY tripname HAVING COUNT(tripname)<4;
-- ---------
-- Query 15
SELECT tripname AS "Bus Trip Name",COUNT(tripname) AS "Current Number of Passengers", bus.licenseplate AS "Current Bus Assigned License Plate",capacity AS "Capacity of Assigned Bus" FROM bustrip,book,bus WHERE bustrip.tripid = book.tripid AND bustrip.licenseplate = bus.licenseplate GROUP BY tripname;
