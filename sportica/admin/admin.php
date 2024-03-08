<?php

require("../lib/lib.php");
require("../lib/db.php");

if (!isset($_SESSION)) {
    session_start();
}

if (isset($_SESSION['id'])) {
    $id = $_SESSION['id'];
    $role = getRole($id);
    if ($role != '[manager]') {
        header('Location: ../index.php');
        die();
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" type="text/css" href="../css/sportica.style.css">
    <link rel="stylesheet" type="text/css" href="../css/admin.style.css">
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
            <table>
                <tr class="vertical">
                    <td>
                        <a class="admin_menu" href="admin.php?manager=users">
                            <span>User Management</span>
                        </a>
                    </td>
                    <td>
                        <a class="admin_menu" href="admin.php?manager=email">
                            <span>Email Server</span>
                        </a>
                    </td>
                    <td>
                        <a class="admin_menu" href="admin.php?manager=config">
                            <span>Settings</span>
                        </a>
                    </td>
                </tr>
            </table>
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
                        $roleButton = "<a class=\"logged\" href=\"admin.php\"><span>Hi, Administrator</span></a>";
                        break;
                }
                echo $roleButton . " &nbsp;&nbsp;&nbsp;&nbsp;" .
                    "<a id=\"signup\" class=\"signup\" href=\"../login/logout.php\"><span>Logout</span></a>";
            } else {
                echo "<a class=\"signin\" href=\"../login/login.php\"><span>Sign In</span></a>" .
                    "><span>Sign Up</span></a>";
            }

            ?>
        </section>
    </section>
</nav>

<section class="main" id="admin">
    <p>
        <?php

        if (isset($_GET['manager'])) {
            switch ($_GET['manager']) {
                case "users":
                    include("admin_users.php");
                    break;
                case "config":
                    include("admin_config.php");
                    break;
                case "email":
                    include("admin_email.php");
                    break;
            }
        } else {
            include("admin_users.php");
        }
        ?>
    </p>
</section>

</body>
</html>