<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Show Trips by Country Page</title>
</head>
<body>
<?php
include 'connectdb.php';
?>
<h1>Here are trips with your selections:</h1>
<ol>
// Programmer Name: 94
//initiate variables for SQL query
<?php
   $whichCountry= $_POST["nation"];
   $query = "SELECT * FROM bustrip WHERE country = '$whichCountry'";
   $result=mysqli_query($connection,$query);
    if (!$result) {
         die("database query2 failed.");
     }
//display result in a readable fashion
    while ($row=mysqli_fetch_assoc($result)) {
        echo "<li>";
        echo $row["tripid"] . " " . $row["startdate"] . " " . $row["enddate"] . " " . $row["country"] ." " . $row["tripname"]. " " . $row["licenseplate"] . " " . "</li>";
     }
     mysqli_free_result($result);
?>
</ol>
<?php
   mysqli_close($connection);
?>
</body>
</html>
