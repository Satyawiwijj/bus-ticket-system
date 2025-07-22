CREATE DATABASE IF NOT EXISTS bus_system;
USE bus_system;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE buses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    route VARCHAR(255),
    time VARCHAR(255),
    seats INT
);

CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    bus_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (bus_id) REFERENCES buses(id)
);
