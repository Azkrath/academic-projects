<?php
require_once("../lib/lib.php");
require_once("../lib/db.php");

$username = $_GET['username'];

echo !existUserField("name", $username);

?>