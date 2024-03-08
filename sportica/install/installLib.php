<?php

require_once("lib/db.php");


function validateWebApplication()
{
    $filename = "config/.htconfig.xml";

    if (!file_exists($filename)) {
        header('Location: install/install.php');
    }
}

function validateDataBase()
{

    loadConfiguration(ConfigFile);

    $host = $GLOBALS['configDataBase']->host;
    $port = $GLOBALS['configDataBase']->port;
    $username = $GLOBALS['configDataBase']->username;
    $password = $GLOBALS['configDataBase']->password;

    $ligacao = mysql_connect("$host:$port", $username, $password);

    $result = mysql_select_db($GLOBALS['configDataBase']->db, $ligacao);
    
    if (!$result) {
        header('Location: install/createDataBase.php');
    }
}

?>
