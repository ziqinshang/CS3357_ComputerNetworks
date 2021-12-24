// Programmer Name: 94
<?php
   $query = "SELECT * FROM bustrip";
   $result = mysqli_query($connection,$query);
   if (!$result) {
        die("databases query failed.");
    }
   while ($row = mysqli_fetch_assoc($result)) {
        echo '<input type="radio" name="nation" value="';
        echo $row["country"];
        echo '">' . $row["country"] . "<br>";
   }
   mysqli_free_result($result);
?>

