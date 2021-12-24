<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Update Trip Page</title>
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
   $whichTrip= $_POST["tripid"];
   $TripName = $_POST["tripname"];
    $StartDate = $_POST["startdate"];
    $EndDate = $_POST["enddate"];
    $URL = $_POST["url"];

   $query1 = "SELECT * FROM bustrip WHERE tripid = $whichTrip ";
$result = mysqli_query($connection, $query1);
//display image
while ($row = mysqli_fetch_assoc($result)){
if($row[urlimage] != "NULL"){
    echo "<img src =" . $row[urlimage].">";
}
else{
    echo "No image found";
}
    }
// Programmer Name: 94
//initiate variables for SQL query
$query = "UPDATE bustrip SET tripname ='$TripName',startdate = '$StartDate',enddate = '$EndDate',urlimage = '$URL' WHERE tripid = $whichTrip ";
   if (!mysqli_query($connection, $query)) {
        die("Error: update failed" . mysqli_error($connection));
    }
   echo "Trip successfully updated!";

   mysqli_close($connection);
?>
</ol>
</body>
</html>
