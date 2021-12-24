// Programmer Name: 94
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
<h1>Here are your trips:</h1>
<ol>
//initiate variables for SQL query
<?php
    $whichTrip= $_POST["tripid"];
    $whichPassenger= $_POST["pickapassenger"];
   $bookingPrice= $_POST["Price"];
    $query = "INSERT INTO book VALUES ($whichPassenger,$whichTrip,$bookingPrice) ";
   if (!mysqli_query($connection, $query)) {
        die("Error: booking add failed" . mysqli_error($connection));
    }
   echo "Booking successfully added!";

   mysqli_close($connection);
?>
</ol>
</body>
</html>
