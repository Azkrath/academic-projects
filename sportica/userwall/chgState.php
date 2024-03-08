<?php
    require_once( "../Lib/db.php" );
    require_once( "../Lib/lib.php" );
    
    $method = $_SERVER['REQUEST_METHOD'];
    if ($method == 'POST') {
        $args = $_POST;
    } elseif ($method == 'GET') {
        $args = $_GET;
    }
    
    $state = $args['state'];
    $id    = $args['id'];
    
    dbConnect(ConfigFile);

    mysql_select_db($GLOBALS['configDataBase']->db, $GLOBALS['ligacao']);
    
    $query = " UPDATE `content-details` SET " .  
             " `state`='$state' " .
             " WHERE `id`='$id' ";

    mysql_query($query, $GLOBALS['ligacao'] );

    $recordsInserted = mysql_affected_rows( $GLOBALS['ligacao'] );
    
    dbDisconnect();
?>
