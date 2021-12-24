<?php
   $query = "SELECT DISTINCT * FROM book, passenger, bustrip WHERE book.passengerid = passenger.passengerid AND bustrip.tripid = book.tripid";
   $result = mysqli_query($connection,$query);
   if (!$result) {
        die("databases query failed.");
    }
// Programmer Name: 94
//initiate variables for SQL query
   while ($row = mysqli_fetch_assoc($result)) {
        echo '<input type="radio" name="bookid" value="';
        echo $row["tripid"];
        echo ",";
        echo $row["passengerid"];
        echo '">' . $row["tripname"] . "   ---   " . $row["firstname"] . " " . $row["lastname"] . " "  . "<br>";
   }
   mysqli_free_result($result);
?>
