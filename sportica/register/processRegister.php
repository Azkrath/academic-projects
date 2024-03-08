<?php
require_once("../lib/lib.php");
require_once("../lib/db.php");
require_once("../lib/PHPMailer/PHPMailerAutoload.php");
require_once("../lib/ReCaptcha/autoload.php");

session_start();

$serverName = $_SERVER['SERVER_NAME'];

$serverPort = 80;
$serverPortSSL = 443;

$name = webAppName();

$baseUrl = "https://" . $serverName . ":" . $serverPortSSL;

$baseNextUrl = $baseUrl . $name;

$first_name = $_POST['first_name'];
$last_name = $_POST['last_name'];
$password = $_POST['second_password'];
$email = $_POST['email'];


dbConnect(ConfigFile);
mysql_select_db($GLOBALS['configDataBase']->db, $GLOBALS['ligacao']);
$query = "SELECT * FROM `captcha-key` WHERE id = 1";
$result = mysql_query($query);
if ($result) {
    $row = mysql_fetch_array($result);
    $secret = $row['secret_key'];
}
dbDisconnect();

$recaptcha = new ReCaptcha\ReCaptcha($secret);
$response = $recaptcha->verify($_POST['g-recaptcha-response'], $_SERVER['REMOTE_ADDR']);

date_default_timezone_set('Etc/UTC');

$mail = new PHPMailer;
$config = getEmailConfig();

$mail->isSMTP();
$mail->Host = $config['host'];
$mail->SMTPAuth = $config['smtp_auth'];
$mail->Username = $config['username'];
$mail->Password = $config['password'];
$mail->SMTPSecure = $config['smtp_secure'];
$mail->Port = $config['port'];

$mail->addAddress($email, $first_name . " " . $last_name);
$mail->setFrom($config['email'], $config['display_name']);
$mail->addReplyTo($config['email'], $config['display_name']);
$mail->isHTML(true);

$accountAdded = false;

$isNewUser = !(existUserField("email", $email));
if (strlen($first_name) > 0 && strlen($last_name) > 0 && strlen($password) > 0 && strlen($email) > 0) {

    if ($response != null && $response->isSuccess()) {
        //echo "Ok - Code is correct<br/>";

        if ($isNewUser) {
            dbConnect(ConfigFile);

            mysql_select_db($GLOBALS['configDataBase']->db, $GLOBALS['ligacao']);

            $query = "INSERT INTO `auth-accounts` (`first_name`, `last_name`, `password`, `email`, `role`, `valid`)" .
                " VALUES ('$first_name', '$last_name','$password', '$email', 2, 0)";
            // echo "SQL statment:\n<br>$query\n<br>";
            mysql_query($query, $GLOBALS['ligacao']);
            $recordsInserted = mysql_affected_rows($GLOBALS['ligacao']);

            $challenge = md5($first_name . $last_name . $password . $email . time());
            $query = "INSERT INTO `auth-challenge` (`id`, `challenge`) VALUES ('" . mysql_insert_id() . "', '$challenge')";
            // echo "SQL statment:\n<br>$query\n<br>";
            mysql_query($query, $GLOBALS['ligacao']);
            $recordsInserted *= mysql_affected_rows($GLOBALS['ligacao']);

            if ($recordsInserted == -1) {
                echo "<h3>Error - Insert of account has failed!</h3>";
            } else {
                echo "<h3>Account added with success.</h3>";

                dbDisconnect();

                $mail->Subject = 'Account Registration';
                $mail->Body = "<h3>Welcome to sportica</h3>" .
                    "<p><a href=\"$baseNextUrl" . "processChallenge.php?challenge=$challenge\">Confirm Account</a></p>";
                $mail->AltBody = "Welcome to sportica\n\n" . "Confirm account\n" .
                    $baseNextUrl . "processChallenge.php?challenge=$challenge";

                if (!$mail->send()) {
                    echo "<h3>Error - Message could not be sent.</h3>";
                    //echo "Mailer Error: " . $mail->ErrorInfo . "<br/>";
                } else {
                    echo '<h3>Confirmation has been sent.</h3>';
                    $accountAdded = true;
                }

                //echo "<br/><a href=\"$baseNextUrl" . "processChallenge.php?challenge=$challenge\">Confirm Account</a>";
            }
        } else
            echo "<h3>Error - Email already exists<h3><";

    } else {
        echo "<h3>Error - Code is incorrect<h3>";
    }

} else
    echo "<h3>Password or email cannot be empty</h3>";

echo "<h3>Redirecting...</h3>";

if ($accountAdded) {
    echo "<META HTTP-EQUIV=\"refresh\" CONTENT=\"2; URL=../login/login.php\">";
} else {
    echo "<META HTTP-EQUIV=\"refresh\" CONTENT=\"5; URL=register.php\">";
}

?>