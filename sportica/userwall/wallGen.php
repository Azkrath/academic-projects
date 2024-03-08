<?php

    require_once( "lib/lib.php" );
    require_once( "lib/db.php" );
    
    $configDetails = getConfiguration();
      
    $name = webAppName();
    
    dbConnect(ConfigFile);
    mysql_select_db($GLOBALS['configDataBase']->db, $GLOBALS['ligacao']);
    
    if (isset($_SESSION['id'])) {
        $query = "SELECT `id`, `fileName`, `publisher`, `description`, `tags`, `pubDate`, `state` FROM `content-details` WHERE `tags` LIKE '%$filter%' ORDER BY `id` DESC";
    } else {
        $query = "SELECT `id`, `fileName`, `publisher`, `description`, `tags`, `pubDate`, `state` FROM `content-details` WHERE `state` = '1' ORDER BY `id` DESC";
    }
   $result = mysql_query($query, $GLOBALS['ligacao']);

    while ($imageData = mysql_fetch_array($result)) {
        $id = $imageData['id'];
        $publisher = $imageData['publisher'];
        $description = $imageData['description'];
        $tags = $imageData['tags'];
        $pubDate = $imageData['pubDate'];
        $state = $imageData['state'];
        if($state == 1) {
            $globe = "sel_globe.png";
            $lock = "lock.png";
        } else if($state == 2) {
            $globe = "globe.png";
            $lock = "sel_lock.png";
        }
        if($pubDate == date("Y-m-d") ) {
            $date = "Today";
        } else if($pubDate == date("Y-m-d", strtotime("yesterday"))) {
            $date = "Yesterday";
        } else {
            $date = $pubDate;
        }
        
        $query2 = "SELECT `first_name`, `last_name` FROM `auth-accounts` WHERE `id`='$publisher'";
        $result2 = mysql_query($query2, $GLOBALS['ligacao']);
        $names = mysql_fetch_array($result2);
        
        $fname = $names['first_name'];
        $lname = $names['last_name'];
        
        $query3 = "SELECT * FROM `content-comments` WHERE `contentId`='$id'";
        $result3 = mysql_query($query3, $GLOBALS['ligacao']);
        
        $showComm = "<div class=\"comm-box\">";
        if (isset($_SESSION['id'])) {
            while ($comments = mysql_fetch_array($result3)) {
                $query4 = "SELECT `first_name`, `last_name` FROM `auth-accounts` WHERE `id`=' " . $comments['publisher'] . "'";
                $result4 = mysql_query($query4, $GLOBALS['ligacao']);
                $names2 = mysql_fetch_array($result4);

                $comm_fname = $names2['first_name'];
                $comm_lname = $names2['last_name'];

                $showComm .= " <div> "
                            . " <p> <span style=\"color:steelblue\">[" . $comm_fname . " " . $comm_lname . "]</span> wrote: ". $comments['contents'] . "</p>"
                            . "</div>";
            }
        }
        $showComm .= "</div>";
        
        if (isset($_SESSION['id']) && $publisher == $_SESSION['id']) {
            $buttons = "<button class=\"sttBtn\" id=\"public" . $id . "\" type=\"button\" onclick=\"change_state2(this, $id)\"><img id=\"pub" . $id . "\" src=\"assets/" . $globe ."\"></button>"
                     . "<button class=\"sttBtn\" id=\"private" . $id ."\" type=\"button\" onclick=\"change_state2(this, $id)\"><img id=\"prt" . $id . "\" src=\"assets/" . $lock ."\"></button>";
        } else {
            $buttons = "";
        }
        
        if (isset($_SESSION['id'])) {
            $showComArea = "<h2 style=\"color: steelblue\">Comments</h2>"
                            . $showComm
                            . "<textarea name=\"comment\" rows=\"4\" cols=\"80\"onclick=\"ClearField(this)\">Insert new comment</textarea>"
                            . "<br>"
                            . "<input type=\"hidden\" name=\"publisher\" value=\"$publisher\">"
                            . "<input type=\"hidden\" name=\"id\" value=\"$id\">"
                            . "<input class=\"styled-button\" width=\"2%\" type=\"submit\" name=\"submit\" value=\"Submit\">";
        } else {
            $showComArea = "";
        }
        
        echo "<form enctype=\"multipart/form-data\" "
            . "action=\"userwall/submitComment.php\" "
            . "method=\"POST\" "
            . "name=\"submitComment\"> "
                . "<div class=\"div-box\" "
                    . "scrolling=\"no\" "
                    . "onload=\"resizeIframe(this)\">"
                    . "<div class=\"div-pub\">" 
                        . $fname . " " . $lname . "<br>"
                        . $date . "<br>"
                    . "</div>"
                    . "<div class=\"div-pub\" style=\"color: #000000\">"
                        . $description
                    . "</div><br/>"
                    . "<div class=\"div-img\">"
                        . "<img src=\"" . $name . "userwall/getFileContents.php?id=$id\" class=\"wall-img\">"
                    . "</div>"
                    . "<div class=\"div-pub\">"
                    . $buttons
                    . $tags
                    . "</div>"
                    . "<div class=\"div-comment\">"
                        . $showComArea
                    . "</div><br>"
                . "</div><br>"
            . "</form>";
    }
    dbDisconnect();
?>
