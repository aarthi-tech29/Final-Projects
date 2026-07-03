CREATE DATABASE CustomerDB;

USE CustomerDB;

CREATE TABLE customers (
    CustomerID INT PRIMARY KEY,
    Name VARCHAR(100),
    Gender VARCHAR(20),
    Age INT,
    City VARCHAR(100),
    State VARCHAR(100),
    Country VARCHAR(100),
    Phone VARCHAR(20),
    Email VARCHAR(100),
    Orders INT,
    TotalPurchase DECIMAL(10,2),
    LastPurchase DATE,
    Occupation VARCHAR(100),
    Income DECIMAL(12,2),
    Membership VARCHAR(50),
    RewardPoints INT,
    Status VARCHAR(20),
    CLV DECIMAL(12,2),
    PurchaseFrequency DECIMAL(10,2),
    Segment VARCHAR(50)
);

SHOW TABLES;
DESCRIBE customers;

SELECT * FROM customers;