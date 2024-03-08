<?php

require_once("install/installLib.php");

validateWebApplication();
validateDataBase();

require_once("lib/lib.php");
require_once("lib/db.php");

if (!isset($_SESSION)) {
    session_start();
}

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" type="text/css" href="css/register.style.css">
    <link rel="stylesheet" type="text/css" href="css/sportica.style.css">
    <link rel="stylesheet" type="text/css" href="css/wall.style.css">
    <link href='http://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css'>
    <title>sportica - Photo Sharing!</title>
    <script language="javascript" type="text/javascript">
        function resizeIframe(obj) {
            obj.style.height = obj.contentWindow.document.body.scrollHeight + 'px';
        }
    </script>
    <script type="text/javascript" src="js/scripts.js"></script>
</head>
<body>

<header>
    <section class="container">
        <div id="header_lc">
            <a href="index.php">sportica</a>
        </div>
        <div id="header_rc">
            <input type="search" name="search" id="search" size="50" autocomplete="on">
            &nbsp;&nbsp;
            <label onclick="search(document.getElementById('search').value)" for="search">search</label>
        </div>
    </section>
</header>

<nav id="row">
    <section class="container">
        <section class="row_lc">
            <?php

            include("ws/GeoIP.php");
            include("ws/CountryInfo.php");

            $geo_ip = new GeoIP();
            $country_info = new CountryInfo();

            $ip = $geo_ip->getIP();
            $country_name = $geo_ip->getCountryName();
            $country_code = $country_info->getCountryISOCode($country_name);
            $country_flag = $country_info->getCountryFlag($country_code);

            echo "<img class=\"flag\" src=\"$country_flag\" width=\"30\" height=\"20\" border=\"1\">";
            echo "<div class=\"geoip\"><span>$ip</span></div>";

            ?>
        </section>
        <section class="row_rc">
            <?php
            if (isset($_SESSION['id'])) {
                $id = $_SESSION['id'];
                $name = getFullName($id);
                $role = getRole($id);

                $roleButton = "";
                switch ($role) {
                    case '[user]':
                        $roleButton = "<div class=\"logged\"><span>Hi, $name</span></div>";
                        break;
                    case '[manager]':
                        $roleButton = "<a class=\"logged\" href=\"admin/admin.php\"><span>Hi, Administrator</span></a>";
                        break;
                }
                echo $roleButton . " &nbsp;&nbsp;&nbsp;&nbsp;" .
                    "<a class=\"signup\" href=\"login/logout.php\"><span>Logout</span></a>";
            } else {
                echo "<a class=\"signin\" href=\"login/login.php\"><span>Sign In</span></a>" .
                    "<a class=\"signup\" href=\"register/register.php\"><span>Sign Up</span></a>";
            }

            ?>
        </section>
    </section>
</nav>

<section class="main">

    <?php
    $authed = include("lib/ensureAuth.php");

    echo "<div id=\"frame\" class=\"wall-box\" >";
    if ($authed == "true") {
        echo "<iframe class=\"frame-box\" "
            . "scrolling=\"no\" "
            . "onload=\"resizeIframe(this)\" "
            . "src=\"upload/formUpload.php\"> "
            . "</iframe><br>";
    }
    if (!isset($_GET['filter'])) {
        $_GET['filter'] = '%';
        $filter = '%';
    } else {
        $filter = $_GET['filter'];
    }
    include("userwall/wallGen.php");
    ?>

</section>

</body>
</html>