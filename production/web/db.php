<?php
$host = getenv('MYSQL_HOST') ?: '127.0.0.1';
$user = getenv('MYSQL_USER') ?: 'root';
$pass = getenv('MYSQL_PASS') ?: '';
$db   = getenv('MYSQL_DB') ?: 'ml';

$conn = new mysqli($host, $user, $pass, $db);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>
