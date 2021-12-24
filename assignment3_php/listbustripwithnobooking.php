// Programmer Name: 94
//initiate variables for SQL query
<?php
   $query = "SELECT DISTINCT bustrip.tripid,tripname FROM bustrip,book WHERE bustrip.tripid NOT IN (SELECT DISTINCT bustrip.tripid FROM bustrip,book WHERE bustrip.tripid = book.tripid)";
   $result = mysqli_query($connection,$query);
   if (!$result) {
        die("databases query failed.");
    }
//display result in a readable fashion
   while ($row = mysqli_fetch_assoc($result)) {
       echo "<li>";
       echo $row["tripid"]  . " " . $row["tripname"] . " " . "</li>";
   }
   mysqli_free_result($result);
?>
