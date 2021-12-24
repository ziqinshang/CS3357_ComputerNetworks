// Programmer Name: 94
//initiate variables for SQL query
<?php
   $query = "SELECT * FROM bustrip";
   $result = mysqli_query($connection,$query);
   if (!$result) {
        die("databases query failed.");
    }
   echo "Who are you looking up? </br>";
   while ($row = mysqli_fetch_assoc($result)) {
       //display result in a readable fashion
        echo '<input type="radio" name="tripid" value="';
        echo $row["tripid"];
        echo '">' . $row["tripname"] . " " . $row["startdate"] . " -- " . $row["enddate"] . " " . "<br>";
   }
   mysqli_free_result($result);
?>
