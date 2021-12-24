// Programmer Name: 94
// The index page for all php files and functionalities
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>David Assignment3</title>
</head>
<body>
<?php
include 'connectdb.php';
?>
<h1>Welcome to david's travel agency</h1>
<h2>Trips we had</h2>
<form action="gettrip.php" method="post">
<?php
   include 'getdata.php';
?>
<input type="submit" value="Get Trip Names">
</form>
<p>
<hr>
<p>
<h2> UPDATE TRIP:</h2>
<form action="updatetrip.php" method="post">
For which Trip: <br>
<?php
include 'getdata2.php';
?>
Trip's Name: <input type="text" name="tripname"><br>
Trip's Start Date (Format: YYYY-MM-DD): <input type="date" name="startdate"><br>
Trip's End Date (Format: YYYY-MM-DD): <input type="date" name="enddate"><br>
Trip's Image URL : <input type="text" name="url"><br>
<input type="submit" value="Update trip">
</form>
<p>
<hr>
<p>
<h2> DELETE TRIP:</h2>
<form action="deletetrip.php" method="post">
For which Trip: <br>
<?php
include 'getdata2.php';
?>
<input type="submit" value="Delete trip">
</form>
<p>
<hr>
<p>
<h2> ADD NEW TRIP:</h2>
<form action="addtrip.php" method="post">
New Trip's id: <input type="text" name="Tripid"><br>
New Trip's Name: <input type="text" name="Tripname"><br>
New Trip's Start Date (Format: YYYY-MM-DD): <input type="date" name="Startdate"><br>
New Trip's End Date (Format: YYYY-MM-DD): <input type="date" name="Enddate"><br>
New Trip's Country: <input type="text" name="Country"><br>
New Trip's Image URL : <input type="text" name="Url"><br>
New Trip's License Plate: <br>
<?php
include 'getplate.php';
?>
<input type="submit" value="Add trip">
</form>
<p>
<hr>
<p>
<h2>  select a country and see all the bus trips from that country:</h2>
<form action="showtripsbycountry.php" method="post">
<?php
include 'getcountry.php';
?>
<input type="submit" value="Show trips">
</form>
<p>
<hr>
<p>
<h2> create a booking:</h2>
<form action="createbooking.php" method="post">
<select name="pickapassenger" id="pickapassenger">
 <option value="1">Select Here</option>
<?php
include 'getpassenger.php';
?>
</select>
<?php
include 'getdata2.php';
?>
New booking's Price : <input type="number" name="Price"><br>
<input type="submit" value="Create booking">
</form>
<p>
<hr>
<p>
<h2> List all the info about the passengers including passport information in order by last name.:</h2>
<?php
include 'getpassengerinfo.php';
?>
<p>
<hr>
<p>
<h2> Select a passenger and see all of his/her bookings.:</h2>
<form action="getpassengerbooking.php" method="post">
<select name="pickapassenger2" id="pickapassenger2">
 <option value="1">Select Here</option>
<?php
include 'getpassenger.php';
?>
</select>
<input type="submit" value="Search for customer">
</form>
<p>
<hr>
<p>
<h2> DELETE BOOKING:</h2>
<form action="deletebooking.php" method="post">
For which Trip: <br>
<?php
include 'getbooking.php';
?>
<input type="submit" value="Delete Booking">
</form>
<p>
<hr>
<p>
<h2> List all the bus trips that dont any bookings yet. :</h2>
<?php
include 'listbustripwithnobooking.php';
?>
<?php
mysqli_close($connection);
?>
</body>
</html>

