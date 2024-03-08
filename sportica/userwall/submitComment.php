<?php
    header('Content-Type: text/html; charset=utf-8');

    require_once( "../Lib/db.php" );
    require_once( "../Lib/lib.php" );
  
    $method = $_SERVER['REQUEST_METHOD'];

    $_contents        = $_POST['comment'];
    $_contentId       = $_POST['id'];
    $_publisher       = $_POST['publisher'];

    $contents         = addslashes( $_contents );
    $contentId        = addslashes( $_contentId );
    $publisher        = addslashes( $_publisher );
        
    $name = webAppName();
    
    dbConnect(ConfigFile);

    mysql_select_db($GLOBALS['configDataBase']->db, $GLOBALS['ligacao']);
    
    $query = "INSERT INTO `content-comments`" .  
            "( `pubDate`, `publisher`, `contents`, `contentId` ) values " .
            "( CURDATE(), '$publisher', '$contents', '$contentId' )";

    mysql_query($query, $GLOBALS['ligacao'] );

    $recordsInserted = mysql_affected_rows( $GLOBALS['ligacao'] );
    
    if ( $recordsInserted==-1 ) {
        $msg = "Insert of comment has failed!";
    }
    else {
        $msg = "Comment added with success.";
    }
    
    echo "    <meta http-equiv=\"REFRESH\" content=\"0;url=../index.php\">\n";
  
    dbDisconnect();
?>