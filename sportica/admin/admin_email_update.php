<?php

require_once("../lib/lib.php");
require_once("../lib/db.php");

$method = $_SERVER['REQUEST_METHOD'];
if ($method == 'POST') {
    $args = $_POST;
} elseif ($method == 'GET') {
    $args = $_GET;
}

$host = $args['host'];
$username = $args['username'];
$password = $args['password'];
$port = $args['port'];
$display_name = $args['display_name'];
$email = $args['email'];


dbConnect(ConfigFile);
mysql_select_db($GLOBALS['configDataBase']->db, $GLOBALS['ligacao']);

$query = "UPDATE `email-config` SET " .
    "host = '$host', " .
    "username = '$username', " .
    "password = '$password', " .
    "port = '$port', " .
    "display_name = '$display_name', " .
    "email = '$email' " .
    " WHERE id = 1";
$result = mysql_query($query);

dbDisconnect();


header('Location: admin.php');
die();

?>