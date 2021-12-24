<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Add Trip Page</title>
</head>
<body>
<?php
   include 'connectdb.php';
?>
<h1>Here are customer's trips:</h1>
<ol>
// Programmer Name: 94
//initiate variables for SQL query
<?php
    $WhichPassenger= $_POST["pickapassenger2"];
$query = "SELECT DISTINCT * FROM book, passenger, bustrip WHERE book.passengerid = $WhichPassenger AND passenger.passengerid = $WhichPassenger AND bustrip.tripid = book.tripid";
$result = mysqli_query($connection,$query);
if (!$result) {
     die("databases query failed.");
 }
//display result in a readable fashion
while ($row = mysqli_fetch_assoc($result)) {
    echo "<li>";
    echo "$" . $row["money"]  . " " . $row["firstname"]. " " . $row["lastname"] ." ". $row["tripname"]. " " . "</li>";
}
mysqli_free_result($result);
?>
</ol>
</body>
</html>
