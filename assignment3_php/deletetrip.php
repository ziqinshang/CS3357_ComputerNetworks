<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Delete Trip Page</title>
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
   $WhichTrip= $_POST["tripid"];
   $query = "DELETE FROM bustrip WHERE tripid = $WhichTrip ";
   if (!mysqli_query($connection, $query)) {
        die("Error: delete failed" . mysqli_error($connection));
    }
   echo "Trip successfully deleted!";

   mysqli_close($connection);
?>
</ol>
</body>
</html>
