<?php

echo "<table class=\"admin_table\">" . "<tr>" .
    "<th><span>Name</span></th>" . "<th><span>Email</span></th>" . "<th><span>Confirmed</span></th>" . "<th><span>Active</span></th>" . "</tr>";

dbConnect(ConfigFile);

mysql_select_db($GLOBALS['configDataBase']->db, $GLOBALS['ligacao']);

$query = "SELECT * FROM `auth-accounts` WHERE role != 1";
$result = mysql_query($query);

if ($result) {
    while ($row = mysql_fetch_array($result)) {
        $first_name = $row['first_name'];
        $last_name = $row['last_name'];
        $email = $row['email'];
        $valid = $row['valid'];
        $active = $row['active'];

        $valid_button = $valid ? 'button_on' : 'button_off';
        $valid_state = $valid ? 'Yes' : 'No';

        $active_button = $active ? 'button_on' : 'button_off';
        $active_state = $active ? 'Yes' : 'No';

        echo "<tr>" .
            "<th>$first_name $last_name</th>" .
            "<th>$email</th>" .
            "<th><a class=\"$valid_button\" href=\"admin_users_valid.php?valid=$valid&email=$email\"><span>$valid_state</span></a></th>" .
            "<th><a class=\"$active_button\" href=\"admin_users_active.php?active=$active&email=$email\"><span>$active_state</span></a></th>" .
            "<th class=\"remove\"><a class=\"remove_button\" href=\"admin_users_remove.php?remove=$email\"><span>Remove</span></a></th>" .
            "</tr>";
    }
}
dbDisconnect();


?>