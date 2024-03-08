<?php

// Global Regular Expressions used in the application HERE

$msgJSInvalidName = "You must enter a name.";
$msgJSInvalidEmail = "Please provide a valid e-mail address";
$msgJSInvalidAlias = "Invalid Name. You can only use characters!";
$msgJSInvalidPwd = "Invalid Password. You need to use at least: 8 characters, 1 numeric, 1 lowercase letter, 1 uppercase letter and 1 special character";
$msgJSUsernameOK  = "Username OK";
$msgJSUsernameNOK = "Username not avaiable";
$msgJSEmailOK  = "Email OK";
$msgJSEmailNOK = "This email was already used";

$filterEmail = "/^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,3})$/";
$filterAlias = "/^([a-zA-Z]{3,16})$/";
$filterPassword = "/^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/";

function loadStrings() {
    echo "msgJSInvalidName = \"" . $GLOBALS[ 'msgJSInvalidName' ] . "\";\n";
    echo "msgJSInvalidEmail = \"" . $GLOBALS[ 'msgJSInvalidEmail' ] . "\";\n" ;
    echo "msgJSInvalidAlias = \"" . $GLOBALS[ 'msgJSInvalidAlias' ] . "\";\n";
    echo "msgJSInvalidPwd = \"" . $GLOBALS[ 'msgJSInvalidPwd' ] . "\";\n";
    echo "msgJSUsernameOK  = \"" . $GLOBALS[ 'msgJSUsernameOK' ] . "\";\n";
    echo "msgJSUsernameNOK = \"" . $GLOBALS[ 'msgJSUsernameNOK' ] . "\";\n";
    echo "msgJSEmailOK  = \"" . $GLOBALS[ 'msgJSEmailOK' ] . "\";\n";
    echo "msgJSEmailNOK = \"" . $GLOBALS[ 'msgJSEmailNOK' ] . "\";\n";
    
    echo "filterAlias = " . $GLOBALS[ 'filterAlias' ] . ";\n" ;
    echo "filterEmail = " . $GLOBALS[ 'filterEmail' ] . ";\n" ;
    echo "filterPassword = " . $GLOBALS[ 'filterPassword' ] . ";\n" ;
}

?>
