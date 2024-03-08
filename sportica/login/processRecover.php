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

$email = $_POST['email'];

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

$mail->setFrom($config['email'], $config['display_name']);
$mail->addReplyTo($config['email'], $config['display_name']);
$mail->isHTML(true);

$existUser = (existUserField("email", $email));

echo "<h3>If account exists, you will receive a message...</h3>";

$message = "";
$messageAlt = "";

if ($existUser) {
    dbConnect(ConfigFile);

    mysql_select_db($GLOBALS['configDataBase']->db, $GLOBALS['ligacao']);

    $query = "SELECT * FROM `auth-accounts` WHERE role !='1' AND email = '$email'";
    $result_account = mysql_query($query);
    if ($result_account) {
        $row = mysql_fetch_array($result_account);
        $id = $row['id'];
        $first_name = $row['first_name'];
        $last_name = $row['last_name'];
        $password = $row['password'];

        $message .= "<p>Your password is: $password</p>";
        $messageAlt .= "Your password is: $password";

        $query = "SELECT * FROM `auth-challenge`WHERE id='$id'";
        $result_challenge = mysql_query($query);
        if ($result_challenge) {
            $row = mysql_fetch_array($result_challenge);
            $challenge = $row['challenge'];

            if (strlen($challenge) > 0) {
                $message .= "<p>And <a href=\"$baseNextUrl" . "../register/processChallenge.php?challenge=$challenge\">Confirm Account</a></p>";
                $messageAlt .= "\n\nAnd confirm account\n" . $baseNextUrl . "../register/processChallenge.php?challenge=$challenge";
            }
        }

        dbDisconnect();

        $mail->addAddress($email, $first_name . " " . $last_name);
        $mail->Subject = 'Account Recovery';
        $mail->Body = "<h3>Welcome to sportica</h3>" . $message;
        $mail->AltBody = "Welcome to sportica\n\n" . $messageAlt;

        if (!$mail->send()) {
            echo "<h3>Error - Message could not be sent.</h3>";
            //echo "Mailer Error: " . $mail->ErrorInfo . "<br/>";
        }

    }
}

echo "<h3>Redirecting...</h3>";
echo "<META HTTP-EQUIV=\"refresh\" CONTENT=\"3; URL=login.php\">";


?>