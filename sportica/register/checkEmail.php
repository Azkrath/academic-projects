<?php
require_once("../lib/lib.php");
require_once("../lib/db.php");

$email = $_GET['email'];

echo !existUserField("email", $email);

?>