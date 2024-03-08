<?php

require_once("../lib/lib.php");
require_once("../lib/db.php");


if (isset($_GET['active']) && isset($_GET['email'])) {

    dbConnect(ConfigFile);
    mysql_select_db($GLOBALS['configDataBase']->db, $GLOBALS['ligacao']);

    $active = !$_GET['active'];
    $email = $_GET['email'];

    $query = "UPDATE `auth-accounts` SET active = '$active'  WHERE email = '$email'";
    $result = mysql_query($query);

    dbDisconnect();
}

header('Location: admin.php?manager=users');
die();

?>