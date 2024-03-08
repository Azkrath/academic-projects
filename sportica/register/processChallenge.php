<?php
require_once("../lib/db.php");

$challenge = $_GET['challenge'];

dbConnect(ConfigFile);

mysql_select_db($GLOBALS['configDataBase']->db, $GLOBALS['ligacao']);

$query = "SELECT * FROM `auth-challenge` WHERE `challenge` = '$challenge'";
$result = mysql_query($query);
//echo "SQL statment:\n<br>$query\n<br>";

if ($result) {
    $row = mysql_fetch_row($result);
    $id = $row[0];
    mysql_free_result($result);

    $query = "UPDATE `auth-accounts` SET `valid`='1' WHERE `id` = '$id'";
    mysql_query($query, $GLOBALS['ligacao']);
    $recordsInserted = mysql_affected_rows($GLOBALS['ligacao']);
    //echo "SQL statment:\n<br>$query\n<br>";

    if ($recordsInserted == -1) {
        echo "<h3>Error - Confirmation Failed</h3>";
    } else {
        $query = "DELETE FROM `auth-challenge` WHERE `challenge` = '$challenge'";
        mysql_query($query, $GLOBALS['ligacao']);
        $recordsInserted = mysql_affected_rows($GLOBALS['ligacao']);
        //echo "SQL statment:\n<br>$query\n<br>";
        echo "<h3>Registration Completed</h3>";
    }

} else {
    echo "Error - Confirmation Failed</h3>";
}

dbDisconnect();

echo "<META HTTP-EQUIV=\"refresh\" CONTENT=\"2; URL=../login/login.php\">";
echo "<h3>Redirecting...</h3>";


?>
