<?php

session_start();

require_once("../lib/lib.php");

$serverName = $_SERVER['SERVER_NAME'];

$serverPort = 80;
$serverPortSSL = 443;

$name = webAppName();

$nextUrl = "https://" . $serverName . ":" . $serverPortSSL . $name . "processLogin.php";

?>

<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/html">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" type="text/css" href="../css/sportica.style.css">
    <link rel="stylesheet" type="text/css" href="../css/register.style.css">
    <link href='http://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css'>
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
                <td class="col_one"><b>Email</b></td>
            </tr>
            <tr>
                <td class="col_one">
                    <input type="email" name="email">
                </td>
            </tr>
        </table>
        <table class="space">
            <tr>
                <td class="col_one"><b>Password</b></td>
            </tr>
            <tr>
                <td class="col_one">
                    <input type="password" name="password">
                </td>
            </tr>
        </table>
        <div class="space"></div>
        <table class="space">
            <tr>
                <td class="col_one">
                    <input class="styled-button" type="submit" value="Login">
                </td>
            </tr>
        </table>
        <table>
            <tr>
                <td class="col_one">
                    <a class="recover" href="recover.php"><span>Recover Password</span></a>
                </td>
            </tr>
        </table>
    </form>


    <section class="title">
        <h1>&nbsp;&nbsp;Login&nbsp;&nbsp;<br/>&nbsp;&nbsp;your account&nbsp;&nbsp;</h1>
    </section>
</section>

<div class="clear"></div>

<?php

if (isset($_SESSION['error'])) {
    echo "<section class=\"error\" id=\"error\">" . $_SESSION['error'] . "</section>";
    $_SESSION['error'] = null;
}
?>

</body>


</html>
