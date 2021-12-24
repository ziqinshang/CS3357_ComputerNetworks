<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Trips We Had</title>
</head>
<body>
<?php
include 'connectdb.php';
?>
<h1>Here are your trips:</h1>
<ol>
// Programmer Name: 94
//initiate variables for SQL query
<?php
   $whichType= $_POST["type"];
    $whichOrder= $_POST["order"];
   $query = "SELECT * FROM bustrip ORDER BY $whichType $whichOrder";
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

