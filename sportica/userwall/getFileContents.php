<?php
  require_once( "../Lib/lib.php" );
  require_once( "../Lib/db.php" );
  
  // TODO validate input data
  $id = $_GET['id'];

  // Read from the data base details about the file
  $fileDetails = getFileDetails( $id );

  $fileName = $fileDetails['fileName'];
  $mimeFileName = $fileDetails['mimeFileName'];
  $typeFileName = $fileDetails['typeFileName'];

  // Pass image contents to the browser
  $fileHandler = fopen($fileName, 'rb');

  header("Content-Type: $mimeFileName/$typeFileName");
  header("Content-Length: " . filesize($fileName));
  fpassthru($fileHandler);
  fclose($fileHandler);
?>