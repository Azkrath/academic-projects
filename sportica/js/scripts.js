function ClearField(thisElement) {
   thisElement.value = "";
}

function readURL(input) {
    var url = input.value;
    var ext = url.substring(url.lastIndexOf('.') + 1).toLowerCase();
    if (input.files && input.files[0]&& (ext === "gif" || ext === "png" || ext === "jpeg" || ext === "jpg")) {
        var reader = new FileReader();

        reader.onload = function (e) {
            document.getElementById("imagepreview").src = e.target.result;
        }

        reader.readAsDataURL(input.files[0]);
    }else{
         document.getElementById("imagepreview").src = '/assets/no_preview.png';
    }
}

function search(search) {
    window.location = "index.php?filter=" + search;
}

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

function change_state(button) {
    var btn = button;
    
    if(btn.id === "public") {
        document.getElementById("pub").src = "../assets/sel_globe.png";
        document.getElementById("prt").src = "../assets/lock.png";
        document.getElementById("state").value = "1";
    } else if(btn.id === "private") {
        document.getElementById("pub").src = "../assets/globe.png";
        document.getElementById("prt").src = "../assets/sel_lock.png";
        document.getElementById("state").value = "2";
    }
}

function change_state2(button, id) {
    var btn = button;
    
    if(btn.id === "public" + id) {
        document.getElementById("pub" + id).src = "assets/sel_globe.png";
        document.getElementById("prt" + id).src = "assets/lock.png";
        
        var args = "state=1&id=" + id;
        
        xmlHttp = GetXmlHttpObject();
        xmlHttp.open("GET", "userwall/chgState.php?" + args, true);
        xmlHttp.onreadystatechange = chgStateReply();
        xmlHttp.send(null);
    } else if(btn.id === "private" + id) {
        document.getElementById("pub" + id).src = "assets/globe.png";
        document.getElementById("prt" + id).src = "assets/sel_lock.png";
        
        var args = "state=2&id=" + id;
        
        xmlHttp = GetXmlHttpObject();
        xmlHttp.open("GET", "userwall/chgState.php?" + args, true);
        xmlHttp.onreadystatechange = chgStateReply();
        xmlHttp.send(null);
    }
}

function chgStateReply() {
     if (xmlHttp.readyState == 4) {
         
     }
}