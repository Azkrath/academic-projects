<?php

function getBrowser()
{
    $userBrowser = '';

    $userAgent = $_SERVER['HTTP_USER_AGENT'];

    //echo $userAgent;

    if (preg_match('/Trident/i', $userAgent)) {
        $userBrowser = "Internet Explorer";
    } elseif (preg_match('/MSIE/i', $userAgent)) {
        $userBrowser = "Internet Explorer";
    } elseif (preg_match('/Firefox/i', $userAgent)) {
        $userBrowser = "Mozilla Firefox";
    } elseif (preg_match('/Safari/i', $userAgent)) {
        $userBrowser = "Apple Safari";
    } elseif (preg_match('/Chrome/i', $userAgent)) {
        $userBrowser = "Google Chrome";
    } elseif (preg_match('/Flock/i', $userAgent)) {
        $userBrowser = "Flock";
    } elseif (preg_match('/Opera/i', $userAgent)) {
        $userBrowser = "Opera";
    } elseif (preg_match('/Netscape/i', $userAgent)) {
        $userBrowser = "Netscape";
    }

    if (preg_match('/Mobile/i', $userAgent)) {
        $userBrowser = "Mobile Device";
    }
    return $userBrowser;
}

function redirectToPage($url, $title, $message, $refresTime)
{
    echo "<html>\n";
    echo "  <head>\n";
    echo "    <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>\n";
    echo "    <meta http-equiv=\"REFRESH\" content=\"$refresTime;url=$url\">\n";
    echo "    <title>$title</title>\n";
    echo "  </head>\n";
    echo "  <body>\n";
    echo "    <p>$message</p>";
    echo "    <p>You will be redirect in $refresTime seconds.</p>";
    echo "  </body>\n";
    echo "</html>";
    exit(1);
}

function redirectToLastPage($title, $refreshTime = 5)
{
    $referer = $_SERVER["HTTP_REFERER"];

    echo "<html>\n";
    echo "  <head>\n";
    echo "    <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>\n";
    echo "    <meta http-equiv=\"REFRESH\" content=\"$refreshTime;url=$referer\">\n";
    echo "    <title>$title</title>\n";
    echo "  </head>\n";
    echo "  <body>\n";
    echo "    <p> Invalid data!";
    echo "    <p> Please fill all the fields marked with *. You will be redirect to the last page in $refreshTime seconds\n";
    echo "  </body>\n";
    echo "</html>";
}

$find;
$replace;

function convertToEntities($str)
{
    global $find;
    global $replace;

    if (($find == NULL) || ($replace == NULL)) {
        $find = array();
        $replace = array();

        foreach (get_html_translation_table(HTML_ENTITIES, ENT_QUOTES) as $key => $value) {
            $find[] = $key;
            $replace[] = $value;
        }
    }

    return str_replace($find, $replace, $str);
}

function webAppName()
{
    $uri = explode("/", $_SERVER['REQUEST_URI']);
    $n = count($uri);
    $webApp = "";
    for ($idx = 0; $idx < $n - 1; $idx++) {
        $webApp .= ($uri[$idx] . "/");
    }

    return $webApp;
}

function prepareHeaders()
{
    list($_SERVER['PHP_AUTH_USER'], $_SERVER['PHP_AUTH_PW']) = explode(':', base64_decode(substr($_SERVER['HTTP_AUTHORIZATION'], 6)));
}

function ensureAuth($redirectPage)
{
    prepareHeaders();

    if (!isset($_SERVER['PHP_AUTH_USER']) || !isset($_SERVER['PHP_AUTH_PW'])) {
        header("Location: $redirectPage");
        exit;
    }
}

function showAuth($authType, $realm, $message)
{
    header("WWW-Authenticate: $authType realm=\"$realm\"");
    header("HTTP/1.0 401 Unauthorized");

    echo $message;
}

function accountIsValid($userName, $password)
{
    $userOk = -1;

    dbConnect(ConfigFile);

    mysql_select_db($GLOBALS['configDataBase']->db, $GLOBALS['ligacao']);

    $query =
        "SELECT * FROM `auth-accounts` " .
        "WHERE `email`='$userName' AND `password`='$password' AND `valid`='1'";
    $result = mysql_query($query, $GLOBALS['ligacao']);

    $numRows = mysql_num_rows($result);

    if ($numRows > 0) {
        $userData = mysql_fetch_array($result);
        $userOk = $userData['id'];
    }
    mysql_free_result($result);

    dbDisconnect();

    return $userOk;
}

function accountIsActive($userName, $password)
{
    $userOk = -1;

    dbConnect(ConfigFile);

    mysql_select_db($GLOBALS['configDataBase']->db, $GLOBALS['ligacao']);

    $query =
        "SELECT * FROM `auth-accounts` " .
        "WHERE `email`='$userName' AND `password`='$password' AND `active`='1'";
    $result = mysql_query($query, $GLOBALS['ligacao']);

    $numRows = mysql_num_rows($result);

    if ($numRows > 0) {
        $userData = mysql_fetch_array($result);
        $userOk = $userData['id'];
    }
    mysql_free_result($result);

    dbDisconnect();

    return $userOk;
}

function existUserField($field, $value)
{
    $exists = true;

    dbConnect(ConfigFile);

    mysql_select_db($GLOBALS['configDataBase']->db, $GLOBALS['ligacao']);

    $query =
        "SELECT * FROM `auth-accounts` " .
        "WHERE `$field`='$value'";
    $result = mysql_query($query, $GLOBALS['ligacao']);

    $numRows = mysql_num_rows($result);

    if ($numRows == 0) {
        $exists = false;
    }

    mysql_free_result($result);

    dbDisconnect();

    return $exists;
}

function getRole($userId)
{
    $userRoles = "";

    dbConnect(ConfigFile);

    mysql_select_db($GLOBALS['configDataBase']->db, $GLOBALS['ligacao']);

    $query =
        "SELECT `r`.`name` FROM `auth-roles` AS `r` INNER JOIN `auth-accounts` " .
        "AS `a` ON `r`.`role` = `a`.`role` WHERE `a`.`id` = '$userId' AND `a`.`valid` = '1' AND `a`.`active` = '1'";

    $result = mysql_query($query, $GLOBALS['ligacao']);

    $isFirst = true;
    $userRoles .= "[";

    while ($userData = mysql_fetch_array($result)) {
        if ($isFirst == true) {
            $isFirst = false;
        } else {
            $userRoles .= ", ";
        }

        $userRoles .= $userData['name'];
    }
    $userRoles .= "]";

    mysql_free_result($result);

    dbDisconnect();

    return $userRoles;
}

function getFullName($userId)
{
    $name = -1;

    dbConnect(ConfigFile);

    mysql_select_db($GLOBALS['configDataBase']->db, $GLOBALS['ligacao']);

    $query = "SELECT * FROM `auth-accounts` WHERE `id`='$userId'";

    $result = mysql_query($query, $GLOBALS['ligacao']);

    $numRows = mysql_num_rows($result);

    if ($numRows > 0) {
        $userData = mysql_fetch_array($result);
        $name = $userData['first_name'] . " " . $userData['last_name'];
    }
    mysql_free_result($result);

    dbDisconnect();

    return $name;
}

function getEmail($userId)
{
    $userEmail = -1;

    dbConnect(ConfigFile);

    mysql_select_db($GLOBALS['configDataBase']->db, $GLOBALS['ligacao']);

    $query = "SELECT `email` FROM `auth-accounts` WHERE `id`='$userId'";

    $result = mysql_query($query, $GLOBALS['ligacao']);

    $numRows = mysql_num_rows($result);

    if ($numRows > 0) {
        $userData = mysql_fetch_array($result);
        $userEmail = $userData['email'];
    }
    mysql_free_result($result);

    dbDisconnect();

    return $userEmail;
}

function getEmailConfig()
{
    $config = -1;

    dbConnect(ConfigFile);

    mysql_select_db($GLOBALS['configDataBase']->db, $GLOBALS['ligacao']);

    $query = "SELECT * FROM `email-config` WHERE `active`='1'";

    $result = mysql_query($query, $GLOBALS['ligacao']);

    $numRows = mysql_num_rows($result);

    if ($numRows > 0) {
        $config = mysql_fetch_array($result);
    }
    mysql_free_result($result);

    dbDisconnect();

    return $config;
}


function logout($authType, $realm, $location)
{
    unset($_SERVER['PHP_AUTH_USER']);
    unset($_SERVER['PHP_AUTH_PW']);
    unset($_SERVER['HTTP_AUTHORIZATION']);

    header("WWW-Authenticate: $authType realm=\"$realm\"");
    header("HTTP/1.0 401 Unauthorized");

    header("Location: $location");
}

function getFileDetails($ids)
{

    $isFirst = true;
    $whereClause = "";

    if (is_array($ids)) {
        foreach ($ids as $id) {
            if ($isFirst == false) {
                $whereClause .= " OR `id`='$id'";
            } else {
                $whereClause .= "`id`='$id'";
                $isFirst = false;
            }
        }
    } else {
        $whereClause = "`id`='$ids'";
    }

    dbConnect(ConfigFile);

    mysql_select_db($GLOBALS['configDataBase']->db, $GLOBALS['ligacao']);

    $query = "SELECT * FROM `content-details` WHERE " . $whereClause;

    $result = mysql_query($query, $GLOBALS['ligacao']);

    $idx = 0;
    $fileData = array();

    while (($fileDataRecord = mysql_fetch_array($result)) != false) {

        $fileData[$idx] = $fileDataRecord;

        ++$idx;
    }

    mysql_free_result($result);
    dbDisconnect();

    if (!is_array($ids)) {
        return $fileData[0];
    } else {
        return $fileData;
    }
}

function getConfiguration()
{
    dbConnect(ConfigFile);
    mysql_select_db($GLOBALS['configDataBase']->db, $GLOBALS['ligacao']);
    $query = "SELECT * FROM `content-config`";
    $result = mysql_query($query, $GLOBALS['ligacao']);
    $configuration = mysql_fetch_array($result);
    mysql_free_result($result);
    dbDisconnect();

    return $configuration;
}

function getStats()
{
    dbConnect(ConfigFile);
    mysql_select_db($GLOBALS['configDataBase']->db, $GLOBALS['ligacao']);

    "SELECT COUNT(DISTINCT `mimeFileName`) FROM `images-details`;";
    "SELECT DISTINCT `mimeFileName` FROM `images-details`;";

    $queryTotal = "SELECT count(*) AS totalFiles FROM `content-details`";
    $queryImages = "SELECT count(*) AS totalImages FROM `content-details` WHERE `mimeFileName`='image'";
    $queryVideos = "SELECT count(*) AS totalVideos FROM `content-details` WHERE `mimeFileName`='video'";
    $queryAudios = "SELECT count(*) AS totalAudios FROM `content-details` WHERE `mimeFileName`='audio'";

    // Total files
    $resultTotal = mysql_query($queryTotal, $GLOBALS['ligacao']);
    $totalData = mysql_fetch_array($resultTotal);
    $stats['numFiles'] = $totalData['totalFiles'];
    mysql_free_result($resultTotal);

    // Image files
    $resultImages = mysql_query($queryImages, $GLOBALS['ligacao']);
    $totalImages = mysql_fetch_array($resultImages);
    $stats['numImages'] = $totalImages['totalImages'];
    mysql_free_result($resultImages);

    // Video files
    $resultVideos = mysql_query($queryVideos, $GLOBALS['ligacao']);
    $totalVideos = mysql_fetch_array($resultVideos);
    $stats['numVideos'] = $totalVideos['totalVideos'];
    mysql_free_result($resultVideos);

    // Audio files
    $resultAudios = mysql_query($queryAudios, $GLOBALS['ligacao']);
    $totaltAudios = mysql_fetch_array($resultAudios);
    $stats['numAudios'] = $totaltAudios['totalAudios'];
    mysql_free_result($resultAudios);

    dbDisconnect();

    return $stats;
}

function showUploadFileError($errorCode)
{
    switch ($errorCode) {
        case UPLOAD_ERR_OK:
            $errorMessage = "($errorCode) There is no error, the file uploaded with success.";
            break;

        case UPLOAD_ERR_INI_SIZE:
            $errorMessage = "($errorCode) The uploaded file exceeds the upload_max_filesize directive in php.ini file.";
            break;

        case UPLOAD_ERR_FORM_SIZE:
            $errorMessage = "($errorCode) The uploaded file exceeds the MAX_FILE_SIZE directive that was specified in the HTML form.";
            break;

        case UPLOAD_ERR_PARTIAL:
            $errorMessage = "($errorCode) The uploaded file was only partially uploaded.";
            break;

        case UPLOAD_ERR_NO_FILE:
            $errorMessage = "($errorCode) No file was uploaded.";
            break;

        case UPLOAD_ERR_NO_TMP_DIR:
            $errorMessage = "($errorCode) Missing a temporary folder. Introduced in PHP 4.3.10 and PHP 5.0.3.";
            break;

        case UPLOAD_ERR_CANT_WRITE:
            $errorMessage = "($errorCode) Failed to write file to disk. Introduced in PHP 5.1.0.";
            break;

        case UPLOAD_ERR_EXTENSION:
            $errorMessage = "($errorCode) A PHP extension stopped the file upload.";
            break;

        default:
            $errorMessage = "($errorCode) No description available.";
            break;
    }

    return $errorMessage;
}

?>