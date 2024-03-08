<?php

require_once("../lib/lib.php");
require_once("../lib/db.php");

$method = $_SERVER['REQUEST_METHOD'];
if ($method == 'POST') {
    $args = $_POST;
} elseif ($method == 'GET') {
    $args = $_GET;
}

$destination = str_replace("\\", "\\\\", $args['destination']);
$max_size = $args['max_size'];

if ($destination != "" && $destination != null && $max_size != "" && $max_size != null) {

    dbConnect(ConfigFile);
    mysql_select_db($GLOBALS['configDataBase']->db, $GLOBALS['ligacao']);

    $query = "UPDATE `content-config` SET destination = '$destination', maxFileSize = '$max_size'  WHERE id = 1";
    $result = mysql_query($query);

    dbDisconnect();
}

header('Location: admin.php');
die();

?>