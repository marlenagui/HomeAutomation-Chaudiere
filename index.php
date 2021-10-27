<?php
// Connect to MySQL
$link = mysql_connect( 'localhost', 'maison', '' );
if ( !$link ) {
  die( 'Could not connect: ' . mysql_error() );
}

// Select the data base
$db = mysql_select_db( 'iotdata', $link );
if ( !$db ) {
  die ( 'Error selecting database 'test' : ' . mysql_error() );
}

// Fetch the data
$query = "
  SELECT from_unixtime(date), value
  FROM iotdata";
$result = mysql_query( $query );

// All good?
if ( !$result ) {
  // Nope
  $message  = 'Invalid query: ' . mysql_error() . "n";
  $message .= 'Whole query: ' . $query;
  die( $message );
}

// Print out rows
while ( $row = mysql_fetch_assoc( $result ) ) {
  echo $row['date'] . ' | ' . $row['value'] . "n";
}

// Close the connection
mysql_close($link);
?>