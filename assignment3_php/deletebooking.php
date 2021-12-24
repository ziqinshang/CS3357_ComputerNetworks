<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Delete Booking Page</title>
</head>
<body>
<?php
   include 'connectdb.php';
?>
<ol>
// Programmer Name: 94
//initiate variables for SQL query
<?php
$option = explode(",", $_POST['bookid']);
$Tripid = $option[0];
$Passengerid = $option[1];
echo "$Tripid";
echo "<br>";
echo "$Passengerid";  
$query = "DELETE FROM book WHERE tripid = $Tripid AND passengerid = $Passengerid";
   if (!mysqli_query($connection, $query)) {
        die("Error: delete failed" . mysqli_error($connection));
    }
   echo "Booking successfully deleted!";

   mysqli_close($connection);
?>
</ol>
</body>
</html>
