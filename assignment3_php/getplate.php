// Programmer Name: 94
//initiate variables for SQL query
<?php
   $query = "SELECT * FROM bustrip";
   $result = mysqli_query($connection,$query);
   if (!$result) {
        die("databases query failed.");
    }
//display result in a readable fashion
   while ($row = mysqli_fetch_assoc($result)) {
        echo '<input type="radio" name="plate" value="';
        echo $row["licenseplate"];
        echo '">' . $row["licenseplate"] . "<br>";
   }
   mysqli_free_result($result);
?>
