// Programmer Name: 94
//initiate variables for SQL query
<?php
   $query = "SELECT * FROM passenger";
   $result = mysqli_query($connection,$query);
   if (!$result) {
        die("databases query failed.");
    }
//display result in a readable fashion
   while ($row = mysqli_fetch_assoc($result)) {
       echo "<option value=". $row[passengerid] . ">" . $row[firstname] . " " . $row[lastname]. "</option>";
   }
   mysqli_free_result($result);
?>
