-- Create the database
CREATE DATABASE Retail_BI;

USE Retail_BI;

-- Create Region table
CREATE TABLE Region
(
    RegionID VARCHAR(10) PRIMARY KEY,
    RegionName VARCHAR(50)
);
DESC Region;

-- Create Branch
CREATE TABLE Branch
(
    BranchID VARCHAR(10) PRIMARY KEY,
    BranchName VARCHAR(100),
    City VARCHAR(50),
    State VARCHAR(50),
    RegionID VARCHAR(10),

    FOREIGN KEY (RegionID)
    REFERENCES Region(RegionID)
);
DESC Branch;

-- Supplier
CREATE TABLE Supplier
(
    SupplierID VARCHAR(10) PRIMARY KEY,
    SupplierName VARCHAR(100),
    ContactPerson VARCHAR(100),
    Phone VARCHAR(15),
    Email VARCHAR(100),
    City VARCHAR(50),
    State VARCHAR(50)
);

-- Category
CREATE TABLE Category
(
    CategoryID VARCHAR(10) PRIMARY KEY,
    CategoryName VARCHAR(100)
);

-- Brand
CREATE TABLE Brand
(
    BrandID VARCHAR(10) PRIMARY KEY,
    BrandName VARCHAR(100)
);

-- Product
CREATE TABLE Product
(
    ProductID VARCHAR(10) PRIMARY KEY,
    ProductName VARCHAR(100),

    CategoryID VARCHAR(10),

    BrandID VARCHAR(10),

    SupplierID VARCHAR(10),

    CostPrice DECIMAL(10,2),

    SellingPrice DECIMAL(10,2),

    FOREIGN KEY(CategoryID)
    REFERENCES Category(CategoryID),

    FOREIGN KEY(BrandID)
    REFERENCES Brand(BrandID),

    FOREIGN KEY(SupplierID)
    REFERENCES Supplier(SupplierID)
);

-- Customer
CREATE TABLE Customer
(
    CustomerID VARCHAR(10) PRIMARY KEY,

    CustomerName VARCHAR(100),

    Gender VARCHAR(10),

    Age INT,

    Phone VARCHAR(15),

    Email VARCHAR(100),

    City VARCHAR(50),

    State VARCHAR(50),

    MembershipType VARCHAR(20)
);

-- Sales
CREATE TABLE Sales
(
    InvoiceID VARCHAR(15) PRIMARY KEY,

    OrderDate DATE,

    CustomerID VARCHAR(10),

    ProductID VARCHAR(10),

    BranchID VARCHAR(10),

    Quantity INT,

    UnitPrice DECIMAL(10,2),

    Discount DECIMAL(10,2),

    Revenue DECIMAL(10,2),

    Cost DECIMAL(10,2),

    Profit DECIMAL(10,2),

    FOREIGN KEY(CustomerID)
    REFERENCES Customer(CustomerID),

    FOREIGN KEY(ProductID)
    REFERENCES Product(ProductID),

    FOREIGN KEY(BranchID)
    REFERENCES Branch(BranchID)
);

-- Inventory
CREATE TABLE Inventory
(
    InventoryID VARCHAR(10) PRIMARY KEY,

    BranchID VARCHAR(10),

    ProductID VARCHAR(10),

    OpeningStock INT,

    ReceivedStock INT,

    SoldStock INT,

    CurrentStock INT,

    ReorderLevel INT,

    FOREIGN KEY(BranchID)
    REFERENCES Branch(BranchID),

    FOREIGN KEY(ProductID)
    REFERENCES Product(ProductID)
);
-- Sales_Target
CREATE TABLE Sales_Target
(
    TargetID VARCHAR(10) PRIMARY KEY,

    BranchID VARCHAR(10),

    TargetMonth VARCHAR(20),

    TargetYear INT,

    TargetAmount DECIMAL(12,2),

    FOREIGN KEY(BranchID)
    REFERENCES Branch(BranchID)
);

-- Calendar
CREATE TABLE Calendar
(
    DateValue DATE PRIMARY KEY,

    Year INT,

    Quarter VARCHAR(10),

    MonthNumber INT,

    MonthName VARCHAR(20),

    WeekNumber INT,

    DayNumber INT
);
SHOW TABLES;

-- empty
SELECT COUNT(*) FROM Region;
SELECT COUNT(*) FROM Branch;
SELECT COUNT(*) FROM Supplier;
SELECT COUNT(*) FROM Category;
SELECT COUNT(*) FROM Brand;
SELECT COUNT(*) FROM Product;
SELECT COUNT(*) FROM Customer;
SELECT COUNT(*) FROM Inventory;
SELECT COUNT(*) FROM Sales_Target;
SELECT COUNT(*) FROM Sales;

SELECT * FROM Region;
SELECT * FROM Branch;
SELECT * FROM Supplier;
SELECT * FROM Category;
SELECT * FROM Brand;
SELECT * FROM Product;
SELECT * FROM Customer;
SELECT * FROM Inventory;
SELECT * FROM Sales_Target;
SELECT * FROM Calendar;


DROP TABLE IF EXISTS Sales;
DROP TABLE IF EXISTS Sales_Target;
DROP TABLE IF EXISTS Inventory;
DROP TABLE IF EXISTS Customer;
DROP TABLE IF EXISTS Product;
DROP TABLE IF EXISTS Brand;
DROP TABLE IF EXISTS Category;
DROP TABLE IF EXISTS Supplier;
DROP TABLE IF EXISTS Branch;
DROP TABLE IF EXISTS Region;
DROP TABLE IF EXISTS Calendar;

SELECT COUNT(*) FROM Region;
SELECT COUNT(*) FROM Branch;
SELECT COUNT(*) FROM Supplier;
SELECT COUNT(*) FROM Category;
SELECT COUNT(*) FROM Brand;
SELECT COUNT(*) FROM Product;
SELECT COUNT(*) FROM Customer;
SELECT COUNT(*) FROM Inventory;
SELECT COUNT(*) FROM Sales_Target;
SELECT COUNT(*) FROM Sales;
SELECT COUNT(*) FROM Calendar;

-- Check Duplicate Invoice IDs
SELECT
    InvoiceID,
    COUNT(*) AS DuplicateCount
FROM Sales
GROUP BY InvoiceID
HAVING COUNT(*) > 1;

-- Check Duplicate Customer IDs
SELECT
    CustomerID,
    COUNT(*) AS DuplicateCount
FROM Customer
GROUP BY CustomerID
HAVING COUNT(*) > 1;

-- Check NULL Values
SELECT *
FROM Sales
WHERE CustomerID IS NULL
   OR ProductID IS NULL
   OR BranchID IS NULL
   OR OrderDate IS NULL;
   
-- Check Invalid Product IDs
SELECT *
FROM Sales
WHERE ProductID NOT IN
(
    SELECT ProductID
    FROM Product
);

-- Check Invalid Customer IDs
SELECT *
FROM Sales
WHERE CustomerID NOT IN
(
    SELECT CustomerID
    FROM Customer
);
-- Check Invalid Branch IDs
SELECT *
FROM Sales
WHERE BranchID NOT IN
(
    SELECT BranchID
    FROM Branch
);
-- Check Inventory Stock
SELECT *
FROM Inventory
WHERE CurrentStock < 0;

-- Find Products Needing Reorder
SELECT
    ProductID,
    CurrentStock,
    ReorderLevel
FROM Inventory
WHERE CurrentStock <= ReorderLevel;

-- Add a New Customer
INSERT INTO Customer
(
    CustomerID,
    CustomerName,
    Gender,
    Age,
    Phone,
    Email,
    City,
    State,
    MembershipType
)
VALUES
(
    'CU006',
    'Karthik Raj',
    'Male',
    29,
    '9876500006',
    'karthik@email.com',
    'Chennai',
    'Tamil Nadu',
    'Gold'
);
SELECT * FROM Customer
WHERE CustomerID='CU006';

-- Update Customer
UPDATE Customer
SET MembershipType='Platinum'
WHERE CustomerID='CU006';
SELECT * FROM Customer
WHERE CustomerID='CU006';

-- Delete Customer
DELETE FROM Customer
WHERE CustomerID='CU006';
SELECT * FROM Customer
WHERE CustomerID='CU006';

-- Search Products
SELECT *
FROM Product
WHERE ProductName LIKE '%Dell%';

-- Search Customers by City
SELECT *
FROM Customer
WHERE City='Chennai';

-- Search Branches
SELECT *
FROM Branch
WHERE State='Tamil Nadu';

-- Search Suppliers
SELECT *
FROM Supplier
WHERE SupplierName LIKE '%Dell%';

-- Count Records
-- Customers:
SELECT COUNT(*) AS TotalCustomers
FROM Customer;
-- Products:
SELECT COUNT(*) AS TotalProducts
FROM Product;

-- Sort Products by Selling Price
-- Highest price first:
SELECT ProductName,
SellingPrice
FROM Product
ORDER BY SellingPrice DESC;
 -- Lowest price first:
 SELECT ProductName,
SellingPrice
FROM Product
ORDER BY SellingPrice ASC;

-- Daily Sales Report
SELECT
    OrderDate,
    SUM(Revenue) AS TotalRevenue,
    SUM(Profit) AS TotalProfit
FROM Sales
GROUP BY OrderDate
ORDER BY OrderDate;

-- Weekly Sales Report
SELECT
    YEAR(OrderDate) AS Year,
    WEEK(OrderDate) AS WeekNo,
    SUM(Revenue) AS TotalRevenue,
    SUM(Profit) AS TotalProfit
FROM Sales
GROUP BY YEAR(OrderDate), WEEK(OrderDate)
ORDER BY Year, WeekNo;

-- Monthly Sales Report
SELECT
    YEAR(OrderDate) AS Year,
    MONTHNAME(OrderDate) AS Month,
    SUM(Revenue) AS TotalRevenue,
    SUM(Profit) AS TotalProfit
FROM Sales
GROUP BY YEAR(OrderDate), MONTH(OrderDate), MONTHNAME(OrderDate)
ORDER BY Year, MONTH(OrderDate);

-- Yearly Sales Report
SELECT
    YEAR(OrderDate) AS Year,
    SUM(Revenue) AS TotalRevenue,
    SUM(Profit) AS TotalProfit
FROM Sales
GROUP BY YEAR(OrderDate);

-- Total Revenue
SELECT
SUM(Revenue) AS TotalRevenue
FROM Sales;

-- Total Profit
SELECT
SUM(Profit) AS TotalProfit
FROM Sales;

-- Total Discount
SELECT
SUM(Discount) AS TotalDiscount
FROM Sales;
-- Gross Margin %
SELECT
ROUND((SUM(Profit)/SUM(Revenue))*100,2)
AS GrossMarginPercentage
FROM Sales;

-- Executive KPI Query
SELECT
SUM(Revenue) AS Revenue,
SUM(Profit) AS Profit,
SUM(Discount) AS Discount,
ROUND((SUM(Profit)/SUM(Revenue))*100,2) AS GrossMargin
FROM Sales;

-- Product-wise Sales\
SELECT
p.ProductName,
SUM(s.Quantity) AS QuantitySold,
SUM(s.Revenue) AS Revenue,
SUM(s.Profit) AS Profit
FROM Sales s
JOIN Product p
ON s.ProductID=p.ProductID
GROUP BY p.ProductName
ORDER BY Revenue DESC;

-- Category-wise Sales
SELECT
c.CategoryName,
SUM(s.Revenue) AS Revenue,
SUM(s.Profit) AS Profit
FROM Sales s
JOIN Product p
ON s.ProductID=p.ProductID
JOIN Category c
ON p.CategoryID=c.CategoryID
GROUP BY c.CategoryName
ORDER BY Revenue DESC;

-- Brand-wise Sales
SELECT
b.BrandName,
SUM(s.Revenue) AS Revenue,
SUM(s.Profit) AS Profit
FROM Sales s
JOIN Product p
ON s.ProductID=p.ProductID
JOIN Brand b
ON p.BrandID=b.BrandID
GROUP BY b.BrandName
ORDER BY Revenue DESC;

-- Branch-wise Sales
SELECT
b.BranchName,
SUM(s.Revenue) AS Revenue,
SUM(s.Profit) AS Profit
FROM Sales s
JOIN Branch b
ON s.BranchID=b.BranchID
GROUP BY b.BranchName
ORDER BY Revenue DESC;

-- Region-wise Sales
SELECT
r.RegionName,
SUM(s.Revenue) AS Revenue,
SUM(s.Profit) AS Profit
FROM Sales s
JOIN Branch b
ON s.BranchID=b.BranchID
JOIN Region r
ON b.RegionID=r.RegionID
GROUP BY r.RegionName
ORDER BY Revenue DESC;

-- Inventory Availability
SELECT
    p.ProductName,
    b.BranchName,
    i.OpeningStock,
    i.ReceivedStock,
    i.SoldStock,
    i.CurrentStock,
    i.ReorderLevel
FROM Inventory i
JOIN Product p
    ON i.ProductID = p.ProductID
JOIN Branch b
    ON i.BranchID = b.BranchID;
    
-- Products Needing Reorder
SELECT
    p.ProductName,
    i.CurrentStock,
    i.ReorderLevel
FROM Inventory i
JOIN Product p
    ON i.ProductID = p.ProductID
WHERE i.CurrentStock <= i.ReorderLevel;

-- Generate Customer Purchase History and Buying Trends
SELECT
    c.CustomerName,
    COUNT(s.InvoiceID) AS TotalOrders,
    SUM(s.Quantity) AS TotalItems,
    SUM(s.Revenue) AS TotalSpent
FROM Customer c
JOIN Sales s
    ON c.CustomerID = s.CustomerID
GROUP BY c.CustomerName
ORDER BY TotalSpent DESC;

-- Requirement 11
-- Identify Top-Selling and Slow-Moving Products
-- Top 10 Selling Products
SELECT
    p.ProductName,
    SUM(s.Quantity) AS QuantitySold,
    SUM(s.Revenue) AS Revenue
FROM Sales s
JOIN Product p
    ON s.ProductID = p.ProductID
GROUP BY p.ProductName
ORDER BY QuantitySold DESC
LIMIT 10;

-- Slow Moving Products
SELECT
    p.ProductName,
    SUM(s.Quantity) AS QuantitySold
FROM Sales s
JOIN Product p
    ON s.ProductID = p.ProductID
GROUP BY p.ProductName
ORDER BY QuantitySold ASC
LIMIT 10;

-- Create Sales Target vs Achievement Reports
SELECT
    b.BranchName,
    st.TargetAmount,
    COALESCE(SUM(s.Revenue),0) AS AchievedSales,
    ROUND(
        (COALESCE(SUM(s.Revenue),0) / st.TargetAmount) * 100,
        2
    ) AS AchievementPercentage
FROM Sales_Target st
JOIN Branch b
    ON st.BranchID = b.BranchID
LEFT JOIN Sales s
    ON st.BranchID = s.BranchID
GROUP BY
    b.BranchName,
    st.TargetAmount;
    
DELETE FROM Sales;
DELETE FROM Calendar;
DELETE FROM Sales_Target;

