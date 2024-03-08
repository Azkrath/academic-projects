<?php

$method = $_SERVER['REQUEST_METHOD'];
if ($method == 'POST') {
    $args = $_POST;
} elseif ($method == 'GET') {
    $args = $_GET;
}

$filename = "../config/.htconfig.xml";

$hostname = $args['hostname'];
$port = $args['port'];
$dbname = $args['dbname'];
$username = $args['username'];
$password = $args['first_password'];


$xmlfile = "<?xml version='1.0' encoding='UTF-8'?>"
    . "<!DOCTYPE DataBase SYSTEM \".htdatabase.dtd\">"
    . "<Config xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" "
    . "xsi:noNamespaceSchemaLocation=\".htconfig.xsd\"> "
    . "<DataBase>"
    . "<host>" . $hostname . "</host>"
    . " <port>" . $port . "</port>"
    . " <db>" . $dbname . "</db>"
    . " <username>" . $username . "</username>"
    . "<password>" . $password . "</password>"
    . "</DataBase>"
    . "</Config>";


$result = @file_put_contents($filename, $xmlfile);

if (!$result) {
    echo "<h3>Could not write file</h3>";
    echo "<h3>Redirecting...</h3>";
    echo "<META HTTP-EQUIV=\"refresh\" CONTENT=\"3; URL=install.php\">";
} else {
    echo "<META HTTP-EQUIV=\"refresh\" CONTENT=\"0; URL=testDataBase.php\">";
}
?>