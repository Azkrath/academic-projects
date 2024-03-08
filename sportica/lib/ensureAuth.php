<?php
  if ( !isset($_SESSION) ) {
    session_start();
  }
  
  if ( !isset($_SESSION['id']) ) {
  	
    $_SESSION[ 'locationAfterAuth' ] = $_SERVER[ 'REQUEST_URI' ]; 
      
    return false;
  } else {
    return true;
  }
?>