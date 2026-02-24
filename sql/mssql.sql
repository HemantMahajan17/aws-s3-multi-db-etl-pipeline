CREATE DATABASE pipelines3tomssql;
USE pipelines3tomssql;

CREATE TABLE Cust_data (
    userId INT,
    id INT PRIMARY KEY,
    title VARCHAR(1000),
    body VARCHAR(8000)
);