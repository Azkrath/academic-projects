<?php

define('ConfigFile', $_SERVER['CONTEXT_DOCUMENT_ROOT'] . DIRECTORY_SEPARATOR . 'config' . DIRECTORY_SEPARATOR . '.htconfig.xml');

$ligacao;
$configDataBase;
$configDataFiles;

function loadConfiguration($configFile)
{
    global $configDataBase;
    global $configDataFiles;

    if (($configDataBase == null) || ($configDataFiles == null)) {
        ($aux = simplexml_load_file($configFile)) or die("Can't read configuration file.");
        $configDataBase = $aux->DataBase[0];
        $configDataFiles = $aux->Files[0];
    }
}

function dbConnect($configFile, $setCharSet = true)
{
    global $configDataBase;
    global $ligacao;

    loadConfiguration($configFile);

    $host = $configDataBase->host;
    $port = $configDataBase->port;
    $username = $configDataBase->username;
    $password = $configDataBase->password;

    $ligacao = mysql_connect("$host:$port", $username, $password)
    or die('Could not connect to data base server');

    if ($setCharSet == true) {
        mysql_set_charset('utf8', $ligacao);
    }
}

function dbDisconnect()
{
    global $ligacao;

    mysql_close($ligacao);
}
