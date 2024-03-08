var xmlHttp;

function GetXmlHttpObject() {
    try {
        return new ActiveXObject("Msxml2.XMLHTTP");
    } catch (e) {
    } // Internet Explorer
    try {
        return new ActiveXObject("Microsoft.XMLHTTP");
    } catch (e) {
    } // Internet Explorer
    try {
        return new XMLHttpRequest();
    } catch (e) {
    } // Firefox, Opera 8.0+, Safari
    alert("XMLHttpRequest not supported");
    return null;
}

function CheckPassword() {
    var password1 = document.getElementById("first_password").value;
    var password2 = document.getElementById("second_password").value;


    if (password1 != password2 || password1 == "" || password1 == null || password2 == "" || password2 == null) {
        document.getElementById("first_password").style.borderColor = "red";
        document.getElementById("second_password").style.borderColor = "red";
    } else {
        document.getElementById("first_password").style.borderColor = "green";
        document.getElementById("second_password").style.borderColor = "green";
    }
}


function CheckEmail() {
    var email = document.getElementById("email").value;
    var args = "email=" + email;

    if (email != "" && email != null) {
        // With HTTP GET method
        xmlHttp = GetXmlHttpObject();
        xmlHttp.open("GET", "checkEmail.php?" + args, true);
        xmlHttp.onreadystatechange = CheckEmailHandleReply;
        xmlHttp.send(null);
    }
    else {
        document.getElementById("email").style.borderColor = "red";
    }
}

function CheckEmailHandleReply() {
    if (xmlHttp.readyState == 4) {
        var isValid = xmlHttp.responseText;

        if (isValid == true)
            document.getElementById("email").style.borderColor = "green";
        else
            document.getElementById("email").style.borderColor = "red";
    }
}


function CheckCaptcha() {
    var captcha = document.getElementById("captcha").value;
    var args = "captcha=" + captcha;

    // With HTTP GET method
    xmlHttp = GetXmlHttpObject();
    xmlHttp.open("GET", "checkCaptcha.php?" + args, true);
    xmlHttp.onreadystatechange = CheckCaptchaHandleReply;
    xmlHttp.send(null);
}

function CheckCaptchaHandleReply() {
    if (xmlHttp.readyState == 4) {
        var isValid = xmlHttp.responseText;

        if (isValid == true)
            document.getElementById("captcha").style.borderColor = "green";
        else
            document.getElementById("captcha").style.borderColor = "red";
    }
}