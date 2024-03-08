<?php

require_once("../lib/lib.php");
require_once("../lib/db.php");

$method = $_SERVER['REQUEST_METHOD'];
if ($method == 'POST') {
    $args = $_POST;
} elseif ($method == 'GET') {
    $args = $_GET;
}

$site_key = $args['site_key'];
$secret_key = $args['secret_key'];

if ($site_key != "" && $site_key != null && $secret_key != "" && $secret_key != null) {

    dbConnect(ConfigFile);
    mysql_select_db($GLOBALS['configDataBase']->db, $GLOBALS['ligacao']);

    $query = "UPDATE `captcha-key` SET site_key = '$site_key', secret_key = '$secret_key'  WHERE id = 1";
    $result = mysql_query($query);

    dbDisconnect();
}

header('Location: admin.php');
die();

?>