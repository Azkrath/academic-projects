<?php

require_once("../lib/lib.php");
require_once("../lib/db.php");

if (isset($_GET['remove'])) {

    dbConnect(ConfigFile);
    mysql_select_db($GLOBALS['configDataBase']->db, $GLOBALS['ligacao']);

    $email = $_GET['remove'];

    $query = "DELETE FROM `auth-accounts` WHERE email = '$email'";
    $result = mysql_query($query);

    dbDisconnect();
}

header('Location: admin.php?manager=users');
die();

?>