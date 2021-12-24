// Programmer Name: 94
<?php
   $query = "SELECT * FROM bustrip";
   $result = mysqli_query($connection,$query);
   if (!$result) {
        die("databases query failed.");
    }
//display result in a readable fashion
while ($row = mysqli_fetch_assoc($result)) {
    echo "<li>";
    echo $row["tripid"] . " " . $row["startdate"] . " " . $row["enddate"] . " " . $row["country"] ." " . $row["tripname"]. " " . $row["licenseplate"] . " " . "</li>";
}
   echo "What are you looking up? </br>";
   echo '<input type="radio" name="type" value="country">Country<br>';
   echo '<input type="radio" name="type" value="tripname">TripName<br>';
    echo "What order would you like? </br>";
    echo '<input type="radio" name="order" value="ASC">Ascending<br>';
    echo '<input type="radio" name="order" value="DESC">Descending<br>';
   mysqli_free_result($result);
?>
