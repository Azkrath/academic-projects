<?php
require_once("../lib/lib.php");
require_once("../lib/db.php");
$configurations = getConfiguration();
?>
<html>
<head>
    <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
    <link rel="stylesheet" type="text/css" href="../css/wall.style.css">
    <link href='http://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css'>
    <script type="text/javascript" src="../js/scripts.js"></script>
</head>

<body>
<form
    enctype="multipart/form-data"
    action="processFormUpload.php"
    method="POST"
    name="FormUpload">

    <br>
    <input type="text" name="title" value="Title of content" onclick="ClearField(this)">
    <button class="sttBtn" id="public" type="button" onclick="change_state(this)"><img id="pub" src="../assets/sel_globe.png"></button>
    <button class="sttBtn" id="private" type="button" onclick="change_state(this)"><img id="prt" src="../assets/lock.png"></button>
    <input type="hidden" name="state" id="state" value="1">
    <br>
    <img class="img_preview" id="imagepreview" src="../assets/no_preview.png">

    <br>
    <textarea name="description" rows="4" cols="50" onclick="ClearField(this)">Description: (Please enter up to 512 characters maximum.)</textarea><br>

    <br>
    <textarea name="tags" rows="4" cols="50" onclick="ClearField(this)">Tags: (Please enter up to 512 characters maximum.)</textarea><br>

    <br>
    <div>
        <input
            type="hidden"
            name="MAX_FILE_SIZE"
            value="<?php echo $configurations['maxFileSize'] ?>">
    </div>
    <div
        class="styled-file-button"
    >
        <text>Choose File</text>
        <input
            class="styled-file-button"
            type="file"
            name="userFile"
            id="imgInput"
            size="64"
            onchange="readURL(this)">
    </div>
    <div>
        <input
            class="styled-file-button-2"
            type="submit"
            name="Submit"
            value="Upload file">
    </div>
    <br>
</form>
</body>
</html>