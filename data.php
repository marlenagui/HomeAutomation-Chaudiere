<!DOCTYPE html>
<html>
<body>
<h1>debut</h1>
 <?php
$servername = "192.168.1.3";
$username = "maison";
$password = "Maison@0103";
$dbname = "maison";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT from_unixtime(date) as date, value FROM iotdata";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // output data of each row
    $prefix = '';
    echo "[\n";
    while($row = $result->fetch_assoc()) {
        // echo " - date: " . $row["date"]. " Value :  " . $row["value"]. "<br>";
  	echo $prefix . " {\n";
  	echo '  "date": "' . $row['date'] . '",' . "\n";
  	echo '  "value": "' . $row['value'] . '"' . "\n";
  	echo " }";
  	$prefix = ",\n";
	}
	echo "\n]";
} else {
    echo "0 results";
}
$conn->close();
?> 
</body>
</html>
