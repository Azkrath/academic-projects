<?php

session_start();

echo($_SESSION['captcha'] == $_GET['captcha']);

?>