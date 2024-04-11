<?php
session_start();

// Check if the form was submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Check if username and password are set
    if (isset($_POST["username"]) && isset($_POST["password"])) {
        // Retrieve username and password from form
        $username = $_POST["username"];
        $password = $_POST["password"];
        
        // Connect to MySQL database
        $conn = mysqli_connect("localhost", "username", "password", "database_name");

        // Check connection
        if (!$conn) {
            die("Connection failed: " . mysqli_connect_error());
        }
        
        // Sanitize input to prevent SQL injection
        $username = mysqli_real_escape_string($conn, $username);
        $password = mysqli_real_escape_string($conn, $password);
        
        // Query to retrieve user from database
        $sql = "SELECT * FROM user WHERE username = '$username' AND password = '$password'";
        $result = mysqli_query($conn, $sql);
        
        // Check if query returned a row
        if (mysqli_num_rows($result) == 1) {
            // Set session variables
            $_SESSION["username"] = $username;
            
            // Redirect to homepage or another page
            header("Location: profilePage.html");
            exit;
        } else {
            // Display error message
            echo "Invalid username or password";
        }
        
        // Close database connection
        mysqli_close($conn);
    }
}
