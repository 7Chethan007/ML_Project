<?php
$host = "127.0.0.1";
$user = "root";
$pass = "Chethan@007";
$db   = "ml";

$conn = new mysqli($host, $user, $pass, $db);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>
