<?php


dbConnect(ConfigFile);
mysql_select_db($GLOBALS['configDataBase']->db, $GLOBALS['ligacao']);

$query = "SELECT * FROM `content-config` WHERE id = 1";
$result = mysql_query($query);
if ($result) {
    $row = mysql_fetch_array($result);
    $image_destination = $row['destination'];
    $image_max_size = $row['maxFileSize'];
}

$query = "SELECT * FROM `captcha-key` WHERE id = 1";
$result = mysql_query($query);
if ($result) {
    $row = mysql_fetch_array($result);
    $site_key = $row['site_key'];
    $secret_key = $row['secret_key'];
}

dbDisconnect();

?>


<form class="config-form" action="admin_config_images.php" method="GET" accept-charset="utf-8">
    <table>
        <tr>
            <td class="col_one"><b>Image Destination</b></td>
        </tr>
        <tr>
            <td class="col_one">
                <input type="text" name="destination" value="<?php echo $image_destination ?>">
            </td>
        </tr>
    </table>
    <table class="space">
        <tr>
            <td class="col_one"><b>Image Max Size (in bytes)</b></td>
        </tr>
        <tr>
            <td class="col_one">
                <input type="number" name="max_size" value="<?php echo $image_max_size ?>">
            </td>
        </tr>
    </table>
    <div class="space"></div>
    <table class="space">
        <tr>
            <td class="col_one">
                <input class="styled-button" type="submit" value="Update Images">
            </td>
        </tr>
    </table>
</form>

<form class="config-form" action="admin_config_captcha.php" method="GET">
    <table>
        <tr>
            <td class="col_one"><b>Site Key</b></td>
        </tr>
        <tr>
            <td class="col_one">
                <input type="text" name="site_key" value="<?php echo $site_key ?>">
            </td>
        </tr>
    </table>
    <table class="space">
        <tr>
            <td class="col_one"><b>Secret Key</b></td>
        </tr>
        <tr>
            <td class="col_one">
                <input type="text" name="secret_key" value="<?php echo $secret_key ?>">
            </td>
        </tr>
    </table>
    <div class="space"></div>
    <table class="space">
        <tr>
            <td class="col_one">
                <input class="styled-button" type="submit" value="Update Captcha">
            </td>
        </tr>
    </table>
</form>