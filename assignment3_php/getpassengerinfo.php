// Programmer Name: 94
//initiate variables for SQL query
<?php
   $query = "SELECT * FROM passenger,passport WHERE passenger.passengerid = passport.passengerid ORDER BY lastname";
   $result = mysqli_query($connection,$query);
   if (!$result) {
        die("databases query failed.");
    }
//display result in a readable fashion
   while ($row = mysqli_fetch_assoc($result)) {
       echo "<li>";
       echo $row["passengerid"]  . " " . $row["firstname"]. " " . $row["lastname"] . " " . $row["passportnum"] . " " . $row["expirydate"] ." " . $row["citizenship"]. " " . $row["birthdate"] . " " . "</li>";
   }
   mysqli_free_result($result);
?>
