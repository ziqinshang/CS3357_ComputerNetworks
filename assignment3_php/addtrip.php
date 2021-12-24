// Programmer Name: 94
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
    $whichTrip= $_POST["Tripid"];
    $whichCountry= $_POST["Country"];
    $TripName = $_POST["Tripname"];
    $StartDate = $_POST["Startdate"];
    $EndDate = $_POST["Enddate"];
    $URL = $_POST["Url"];
   $LicensePlate= $_POST["plate"];
    $query = "INSERT INTO bustrip VALUES ('$whichTrip','$StartDate','$EndDate','$whichCountry','$TripName','$LicensePlate','$URL')";
   if (!mysqli_query($connection, $query)) {
        die("Error: add failed" . mysqli_error($connection));
    }
   echo "Trip successfully added!";

   mysqli_close($connection);
?>
</ol>
</body>
</html>
