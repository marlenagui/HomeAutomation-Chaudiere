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

$sql = "SELECT from_unixtime(date) as date, function, severity, text FROM log where date > '2016-11-23 08:50:00'";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
        echo "" .  $row["date"] . "|" . $row["function"] . "|" . $row["severity"] . "|" . $row["text"] . "<br>";
    }
} else {
    echo "0 results";
}
$conn->close();
?>
</body>
</html>

