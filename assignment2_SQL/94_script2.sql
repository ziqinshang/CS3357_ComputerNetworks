USE 94_assign2db;
-- ---------
-- Insert data into bus
SELECT * FROM bus;
LOAD DATA LOCAL INFILE 'loaddatafall2021.txt' INTO TABLE bus
FIELDS TERMINATED BY ',';
SELECT * FROM bus;
-- ---------
-- Insert data into passenger
SELECT * FROM passenger;
INSERT INTO passenger VALUES('11','Homer', 'Simpson');
INSERT INTO passenger VALUES('22','Marge', 'Simpson');
INSERT INTO passenger VALUES('33','Bart', 'Simpson');
INSERT INTO passenger VALUES('34','Lisa', 'Simpson');
INSERT INTO passenger VALUES('35','Maggie', 'Simpson');
INSERT INTO passenger VALUES('44','Ned', 'Flanders');
INSERT INTO passenger VALUES('45','Todd', 'Flanders');
INSERT INTO passenger VALUES('66','Heidi', 'Klum');
INSERT INTO passenger VALUES('77','Michael', 'Scott');
INSERT INTO passenger VALUES('78','Dwight', 'Schrute');
INSERT INTO passenger VALUES('79','Pam', 'Beesly');
INSERT INTO passenger VALUES('80','Creed', 'Bratton');
INSERT INTO passenger VALUES('99','Michael', 'Jordan');
SELECT * FROM passenger;
-- ---------
-- Insert data into passport
SELECT * FROM passport;
INSERT INTO passport(passportnum,citizenship,expirydate,birthdate,passengerid)
VALUES('US10','USA','2025-01-01','1970-02-19','11');
INSERT INTO passport(passportnum,citizenship,expirydate,birthdate,passengerid) VALUES('US12','USA','2025-01-01','1972-08-12','22');
INSERT INTO passport(passportnum,citizenship,expirydate,birthdate,passengerid) VALUES('US13','USA','2025-01-01','2001-05-12','33');
INSERT INTO passport(passportnum,citizenship,expirydate,birthdate,passengerid) VALUES('US14','USA','2025-01-01','2004-03-19','34');
INSERT INTO passport(passportnum,citizenship,expirydate,birthdate,passengerid) VALUES('US15','USA','2025-01-01','2012-09-17','35');
INSERT INTO passport(passportnum,citizenship,expirydate,birthdate,passengerid) VALUES('US22','USA','2030-04-04','1950-06-11','44');
INSERT INTO passport(passportnum,citizenship,expirydate,birthdate,passengerid) VALUES('US23','USA','2018-03-03','1940-06-24','45');
INSERT INTO passport(passportnum,citizenship,expirydate,birthdate,passengerid) VALUES('GE11','Germany','2027-01-01','1970-07-12','66');
INSERT INTO passport(passportnum,citizenship,expirydate,birthdate,passengerid) VALUES('US88','Canada','2030-02-13','1979-04-25','77');
INSERT INTO passport(passportnum,citizenship,expirydate,birthdate,passengerid) VALUES('US89','Canada','2022-02-02','1976-04-08','78');
INSERT INTO passport(passportnum,citizenship,expirydate,birthdate,passengerid) VALUES('US90','Italy','2020-02-28','1980-04-04','79');
INSERT INTO passport(passportnum,citizenship,expirydate,birthdate,passengerid) VALUES('US91','Germany','2030-01-01','1959-02-02','80');
INSERT INTO passport(passportnum,citizenship,expirydate,birthdate,passengerid) VALUES('US45','USA','2099-01-01','1999-07-15','99');
SELECT * FROM passport;
-- ---------
-- Insert data into bustrip
SELECT * FROM bustrip;
INSERT INTO bustrip(tripid,tripname,startdate,enddate,country,licenseplate) VALUES('1', "Castles of Germany", '2022-01-01', '2022-01-17', 'Germany', 'VAN1111');
INSERT INTO bustrip(tripid,tripname,startdate,enddate,country,licenseplate) VALUES('2', "Tuscany Sunsets", '2022-03-03', '2022-03-14', 'Italy', 'TAXI222');
INSERT INTO bustrip(tripid,tripname,startdate,enddate,country,licenseplate) VALUES('3', "California Wines", '2022-05-05', '2022-05-10', 'USA', 'VAN2222');
INSERT INTO bustrip(tripid,tripname,startdate,enddate,country,licenseplate) VALUES('4', "Beaches Galore", '2022-04-04', '2022-04-14', 'Bermuda', 'TAXI222');
INSERT INTO bustrip(tripid,tripname,startdate,enddate,country,licenseplate) VALUES('5', "Cottage Country", '2022-06-01', '2022-06-22', 'Canada', 'CAND123');
INSERT INTO bustrip(tripid,tripname,startdate,enddate,country,licenseplate) VALUES('6', "Arrivaderci Roma", '2022-07-05', '2022-07-15', 'Italy', 'TAXI111');
INSERT INTO bustrip(tripid,tripname,startdate,enddate,country,licenseplate) VALUES('7', "Shetland and Orkney", '2022-09-09', '2022-09-29', 'UK', 'TAXI111');
INSERT INTO bustrip(tripid,tripname,startdate,enddate,country,licenseplate) VALUES('8',
"Disney World and Sea World", '2022-06-10', '2022-06-20', 'USA', 'VAN2222');
INSERT INTO bustrip(tripid,tripname,startdate,enddate,country,licenseplate) VALUES('9', 
"Trip of Tokyo", '2018-06-10', '2018-06-20', 'Japan', 'VAN2222');
INSERT INTO bustrip(tripid,tripname,startdate,enddate,country,licenseplate) VALUES('10', "Trip to Cuba", '2019-06-10', '2019-06-20', 'Cuba', 'VAN2222');
SELECT * FROM bustrip;
-- ---------
-- Insert data into book
SELECT * FROM book;
INSERT INTO book VALUES('11','1','500');
INSERT INTO book VALUES('22','1','500');
INSERT INTO book VALUES('33','1','200');
INSERT INTO book VALUES('34','1','200');
INSERT INTO book VALUES('35','1','200');
INSERT INTO book VALUES('66','1','600.99');
INSERT INTO book VALUES('44','8','400');
INSERT INTO book VALUES('45','8','200');
INSERT INTO book VALUES('78','4','600');
INSERT INTO book VALUES('80','4','600');
INSERT INTO book VALUES('78','1','550');
INSERT INTO book VALUES('33','8','300');
INSERT INTO book VALUES('34','8','300');
INSERT INTO book VALUES('11','6','600');
INSERT INTO book VALUES('22','6','600');
INSERT INTO book VALUES('33','6','100');
INSERT INTO book VALUES('34','6','100');
INSERT INTO book VALUES('35','6','100');
INSERT INTO book VALUES('11','7','300');
INSERT INTO book VALUES('44','7','400');
INSERT INTO book VALUES('77','7','500');
INSERT INTO book VALUES('99','10','1000');
SELECT * FROM book;
SELECT * FROM passport;
UPDATE passport,passenger SET citizenship = 'Germany' WHERE firstname = 'Dwight' AND passport.passengerid=passenger.passengerid;
SELECT * FROM passport;
SELECT * FROM bustrip;
UPDATE bustrip SET licenseplate = 'VAN1111' WHERE country = 'USA';
SELECT * FROM bustrip;
