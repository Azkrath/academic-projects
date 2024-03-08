<?php

require_once("../lib/lib.php");
require_once("../lib/db.php");

loadConfiguration(ConfigFile);

$host = $configDataBase->host;
$port = $configDataBase->port;
$username = $configDataBase->username;
$password = $configDataBase->password;

$ligacao = @mysql_connect("$host:$port", $username, $password);

if ($ligacao) {
    echo "<script>"
        . "var ok = window.confirm(\"DataBase already exists. Do you want to use this DataBase?\");"
        . "if(ok) { window.location.href = '../index.php'"
        . " } else { window.location.href = 'install.php' }"
        . "</script>";
} else {
    echo "<h3>DataBase not created. Redirecting...</h3>";
    echo "<META HTTP-EQUIV=\"refresh\" CONTENT=\"2; URL=createDataBase.php\">";
}
?>

