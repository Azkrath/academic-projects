<?php
require_once("../lib/lib.php");
require_once("../lib/db.php");

$method = $_SERVER['REQUEST_METHOD'];
if ($method == 'POST') {
    $args = $_POST;
} elseif ($method == 'GET') {
    $args = $_GET;
}

loadConfiguration(ConfigFile);

# local database admin
$host = $configDataBase->host;
$db = $configDataBase->db;
$port = $configDataBase->port;
$username = $configDataBase->username;
$password = $configDataBase->password;

# mysql root
$sqlpath = $args['sqlpath'];
$adminuser = $args['dbadminuser'];
$adminpwd = $args['first_password'];


$user_agent = getenv("HTTP_USER_AGENT");
if (strpos($user_agent, "Win") !== FALSE)
    $os = $sqlpath . 'mysql';
else
    $os = $sqlpath . './mysql';

$access_script = "CREATE DATABASE IF NOT EXISTS " . $db .
    " CHARACTER SET utf8" .
    " COLLATE utf8_unicode_ci;" .

    " CREATE USER '" . $username . "'@'%'" .
    " IDENTIFIED BY '" . $password . "';" .

    " GRANT USAGE ON *.* TO '" . $username . "'@'%'" .
    " IDENTIFIED BY '" . $password . "'" .
    " WITH MAX_QUERIES_PER_HOUR 0" .
    " MAX_CONNECTIONS_PER_HOUR 0" .
    " MAX_UPDATES_PER_HOUR 0" .
    " MAX_USER_CONNECTIONS 0;" .

    "GRANT ALL PRIVILEGES ON " . $db . ".* TO '" . $username . "'@'%';";

$query1 = ' --execute="' . $access_script;
$command1 = $os . ' --user=' . $adminuser . ' --password=' . $adminpwd . $query1 . '"';
$output = system($command1, $retval);

$install_script = "install_script.sql";
$query2 = ' --execute="SOURCE ' . $install_script;
$command2 = $os . ' --user=' . $adminuser . ' --password=' . $adminpwd . " --database=" . $db . $query2 . '"';
$output = system($command2, $retval);


if ($retval) {
    echo "<h3>Something when terribly wrong.Redirecting...</h3>";
    echo "<META HTTP-EQUIV=\"refresh\" CONTENT=\"2; URL=createDataBase.php\">";
} else {
    echo "<h3>DataBase created with success!</h3>";
    echo "<META HTTP-EQUIV=\"refresh\" CONTENT=\"2; URL=../index.php\">";
}


?>

