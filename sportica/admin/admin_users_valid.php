<?php

require_once("../lib/lib.php");
require_once("../lib/db.php");

if (isset($_GET['valid']) && isset($_GET['email'])) {

    dbConnect(ConfigFile);
    mysql_select_db($GLOBALS['configDataBase']->db, $GLOBALS['ligacao']);

    $valid = !$_GET['valid'];
    $email = $_GET['email'];

    $query = "UPDATE `auth-accounts` SET valid = '$valid'  WHERE email = '$email'";
    $result = mysql_query($query);

    dbDisconnect();
}

header('Location: admin.php?manager=users');
die();

?>