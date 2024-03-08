<?php
require_once("../lib/lib.php");
require_once("../lib/db.php");

header('Content-Type: text/html; charset=utf-8');

$serverName = $_SERVER['SERVER_NAME'];

$serverPort = 80;

$name = webAppName();

$baseUrl = "http://" . $serverName . ":" . $serverPort;

$baseNextUrl = $baseUrl . $name;

$method = $_SERVER['REQUEST_METHOD'];
if ($method == 'POST') {
    $args = $_POST;
} elseif ($method == 'GET') {
    $args = $_GET;
}

$username = $args['email'];
$password = $args['password'];

$userId = accountIsValid($username, $password);
$isActive = accountIsActive($username, $password);

session_start();
if ($userId > 0) {
    if ($isActive > 0) {
        $_SESSION['username'] = $username;
        $_SESSION['id'] = $userId;
        $_SESSION['error'] = null;

        if (isset($_SESSION['locationAfterAuth'])) {
            $baseNextUrl = $baseUrl;
            $nextUrl = $_SESSION['locationAfterAuth'];
        } else {
            $nextUrl = "../index.php";
        }
    } else {
        $_SESSION['error'] = "&nbsp;&nbsp;Account suspended !!!";
        $nextUrl = "login.php";
    }
} else {
    $_SESSION['error'] = "&nbsp;&nbsp;Account not found or wrong password !!!";
    $nextUrl = "login.php";
}

header("Location: " . $baseNextUrl . $nextUrl);

?>