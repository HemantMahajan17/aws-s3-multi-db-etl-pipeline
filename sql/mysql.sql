CREATE DATABASE pipelines3tomysql;
USE pipelines3tomysql;

CREATE TABLE Cust_data (
    userId INT,
    id INT PRIMARY KEY,
    title VARCHAR(1000),
    body VARCHAR(8000)
);