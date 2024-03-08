<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" type="text/css" href="../css/register.style.css">
    <link rel="stylesheet" type="text/css" href="../css/sportica.style.css">
    <link rel="stylesheet" type="text/css" href="../css/wall.style.css">
    <link href='http://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css'>
    <title>sportica - Photo Sharing!</title>
    <script language="javascript" type="text/javascript">
        function resizeIframe(obj) {
            obj.style.height = obj.contentWindow.document.body.scrollHeight + 'px';
        }
    </script>
    <script type="text/javascript" src="../js/scripts.js"></script>
    <script type="text/javascript" src="../js/register.js"></script>
</head>
<body>
<header>
    <section class="container">
        <div id="header_lc">
            <a>sportica</a>
        </div>
    </section>
</header>
<section class="main">
    <div class="padding-top"></div>
    <form class="config-form" action="processDBCreation.php" method="POST">
        <table class="space">
            <tr>
                <td class="col_one"><b>SQL Path</b></td>
            </tr>
            <tr>
                <td class="col_one">
                    <input type="text" id="sqlpath" name="sqlpath">
                </td>
            </tr>
        </table>
        <table class="space">
            <tr>
                <td class="col_one"><b>Indicate DB Admin Username</b></td>
            </tr>
            <tr>
                <td class="col_one">
                    <input type="text" id="dbadminuser" name="dbadminuser">
                </td>
            </tr>
        </table>
        <table class="space">
            <tr>
                <td class="col_one"><b>Indicate DB Admin Password</b></td>
            </tr>
            <tr>
                <td class="col_one">
                    <input type="password" id="first_password" name="first_password">
                </td>
            </tr>
        </table>
        <table class="space">
            <tr>
                <td class="col_one"><b>Re-type DB Admin Password</b></td>
            </tr>
            <tr>
                <td class="col_one">
                    <input type="password" id="second_password" name="second_password" onblur="CheckPassword()">
                </td>
            </tr>
        </table>
        <div class="space"></div>
        <table class="space">
            <tr>
                <td class="col_one">
                    <input class="styled-button" type="submit" value="Create DataBase">
                </td>
            </tr>
        </table>
    </form>

    <section class="title">
        <h1>&nbsp;&nbsp;Create&nbsp;&nbsp;<br/>&nbsp;&nbsp;the DataBase&nbsp;&nbsp;</h1>
    </section>
</section>
</body>
</html>