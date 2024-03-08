<?php

$config = getEmailConfig();

$host = $config['host'];
$username = $config['username'];
$password = $config['password'];
$port = $config['port'];
$display_name = $config['display_name'];
$email = $config['email'];

?>

<form class="config-form" action="admin_email_update.php" method="GET" accept-charset="utf-8">
    <table>
        <tr>
            <td class="col_one"><b>Username</b></td>
        </tr>
        <tr>
            <td class="col_one">
                <input type="text" name="username" value="<?php echo $username ?>">
            </td>
        </tr>
    </table>
    <table class="space">
        <tr>
            <td class="col_one"><b>Password</b></td>
        </tr>
        <tr>
            <td class="col_one">
                <input type="text" name="password" value="<?php echo $password ?>">
            </td>
        </tr>
    </table>
    <table class="space">
        <tr>
            <td class="col_one"><b>SMTP Host</b></td>
        </tr>
        <tr>
            <td class="col_one">
                <input type="text" name="host" value="<?php echo $host ?>">
            </td>
        </tr>
    </table>
    <table class="space">
        <tr>
            <td class="col_one"><b>SMTP Port</b></td>
        </tr>
        <tr>
            <td class="col_one">
                <input type="text" name="port" value="<?php echo $port ?>">
            </td>
        </tr>
    </table>
    <table class="space">
        <tr>
            <td class="col_one"><b>Display Name</b></td>
        </tr>
        <tr>
            <td class="col_one">
                <input type="text" name="display_name" value="<?php echo $display_name ?>">
            </td>
        </tr>
    </table>
    <table class="space">
        <tr>
            <td class="col_one"><b>Email</b></td>
        </tr>
        <tr>
            <td class="col_one">
                <input type="text" name="email" value="<?php echo $email ?>">
            </td>
        </tr>
    </table>
    <div class="space"></div>
    <table class="space">
        <tr>
            <td class="col_one">
                <input class="styled-button" type="submit" value="Update Email Server">
            </td>
        </tr>
    </table>
</form>
