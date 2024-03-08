<?php

require_once("../lib/lib.php");
require_once("../lib/db.php");

$serverName = $_SERVER['SERVER_NAME'];

$serverPortSSL = 443;
$serverPort = 80;

$name = webAppName();

$nextUrl = "https://" . $serverName . ":" . $serverPortSSL . $name . "processRegister.php";

dbConnect(ConfigFile);
mysql_select_db($GLOBALS['configDataBase']->db, $GLOBALS['ligacao']);
$query = "SELECT * FROM `captcha-key` WHERE id = 1";
$result = mysql_query($query);
if ($result) {
    $row = mysql_fetch_array($result);
    $siteKey = $row['site_key'];
}
dbDisconnect();

?>

<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/html">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" type="text/css" href="../css/sportica.style.css">
    <link rel="stylesheet" type="text/css" href="../css/register.style.css">
    <link href='http://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css'>
    <script src='../js/register.js'></script>
    <script src='https://www.google.com/recaptcha/api.js'></script>
    <title>sportica - Photo Sharing!</title>
</head>
<body>

<header>
    <section class="container">
        <div id="header_lc">
            <a href="../index.php">sportica</a>
        </div>
    </section>
</header>

<nav id="row">
    <section class="container">
        <section class="row_lc">

        </section>
    </section>
</nav>

<section class="main">
    <div class="padding-top"></div>
    <form class="account-form" action="<?php echo $nextUrl ?>" method="POST">
        <table>
            <tr>
                <td class="col_two"><b>First Name</b></td>
                <td class="col_two"><b>Last Name</b></td>
            </tr>
            <tr>
                <td class="col_two">
                    <input type="text" id="first_name" name="first_name">
                </td>
                <td class="col_two">
                    <input type="text" id="last_name" name="last_name">
                </td>
            </tr>
        </table>
        <table class="space">
            <tr>
                <td class="col_one"><b>Choose a Password</b></td>
            </tr>
            <tr>
                <td class="col_one">
                    <input type="password" id="first_password" name="first_password">
                </td>
            </tr>
        </table>
        <table class="space">
            <tr>
                <td class="col_one"><b>Re-type Password</b></td>
            </tr>
            <tr>
                <td class="col_one">
                    <input type="password" id="second_password" name="second_password" onblur="CheckPassword()">
                </td>
            </tr>
        </table>
        <table class="space">
            <tr>
                <td class="col_one"><b>Contact Email</b></td>
            </tr>
            <tr>
                <td class="col_one">
                    <input type="email" id="email" name="email" onblur="CheckEmail()">
                </td>
            </tr>
        </table>
        <table class="space">
            <tr>
                <td class="col_one"><b>Verify your Registration</b></td>
            </tr>
            <tr>
                <td class="col_one">
                    <div class="g-recaptcha" data-sitekey="<?php echo $siteKey ?>"></div>
                </td>
            </tr>
        </table>
        <div class="space"></div>
        <table class="space">
            <tr>
                <td class="col_one">
                    <input class="styled-button" type="submit" value="Create Account">
                </td>
            </tr>
        </table>
    </form>

    <section class="title">
        <h1>&nbsp;&nbsp;Create&nbsp;&nbsp;<br/>&nbsp;&nbsp;a new account&nbsp;&nbsp;</h1>
    </section>
</section>


</body>
</html>
