DROP DATABASE IF EXISTS my_record_shop;
CREATE DATABASE my_record_shop;
USE my_record_shop;


DROP TABLE IF EXISTS `Genre`;
CREATE TABLE IF NOT EXISTS `Genre` (
    `GenreID` INT NOT NULL AUTO_INCREMENT,
    `GenreName` VARCHAR(100) NOT NULL,
    `Description` TEXT,
    PRIMARY KEY (`GenreID`),
    UNIQUE KEY `GenreName_UNIQUE` (`GenreName`)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `Record_Label`;
CREATE TABLE IF NOT EXISTS `Record_Label` (
    `RecordLabelID` INT NOT NULL AUTO_INCREMENT,
    `LabelName` VARCHAR(255) NOT NULL,
    `FoundedYear` INT NOT NULL,
    `Country` VARCHAR(100) NOT NULL,
    `Website` VARCHAR(255),
    PRIMARY KEY (`RecordLabelID`),
    UNIQUE INDEX `LabelName_UNIQUE` (`LabelName`)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `Band`;
CREATE TABLE IF NOT EXISTS `Band` (
    `BandID` INT NOT NULL AUTO_INCREMENT,
    `BandName` VARCHAR(255) NOT NULL,
    `FoundedYear` INT NOT NULL,
    `GenreID` INT,
    `Country` VARCHAR(100),
    `RecordLabelID` INT,
    PRIMARY KEY (`BandID`),
    UNIQUE KEY `BandName_UNIQUE` (`BandName`),
    INDEX `fk_Band_RecordLabel_idx` (`RecordLabelID`),
    INDEX `fk_Band_Genre_idx` (`GenreID`),
    CONSTRAINT `fk_Band_RecordLabel`
        FOREIGN KEY (`RecordLabelID`)
        REFERENCES `Record_Label` (`RecordLabelID`)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    CONSTRAINT `fk_Band_Genre`
        FOREIGN KEY (`GenreID`)
        REFERENCES `Genre` (`GenreID`)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `Album`;
CREATE TABLE IF NOT EXISTS `Album` (
    `AlbumID` INT NOT NULL AUTO_INCREMENT,
    `Title` VARCHAR(255) NOT NULL,
    `ReleaseDate` DATE NOT NULL,
    `Price` DECIMAL(10,2) NOT NULL CHECK (Price > 0),
    `Format` ENUM('Vinyl', 'CD', 'Cassette', 'Digital') NOT NULL,
    `BandID` INT NOT NULL,
    PRIMARY KEY (`AlbumID`),
    UNIQUE KEY `Band_Title_UNIQUE` (`BandID`, `Title`),
    INDEX `fk_Album_Band_idx` (`BandID`),
    CONSTRAINT `fk_Album_Band`
        FOREIGN KEY (`BandID`)
        REFERENCES `Band` (`BandID`)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `Customers`;
CREATE TABLE IF NOT EXISTS `Customers` (
    `CustomerID` INT NOT NULL AUTO_INCREMENT,
    `FirstName` VARCHAR(255) NOT NULL,
    `LastName` VARCHAR(255) NOT NULL,
    `Email` VARCHAR(255) NOT NULL,
    `Phone` VARCHAR(12) CHECK (Phone REGEXP '^[0-9]{3}-[0-9]{3}-[0-9]{4}$'),
    `BirthDate` DATE,
    `LoyaltyPoints` INT DEFAULT 0 CHECK (LoyaltyPoints >= 0),
    `GenreID` INT,
    PRIMARY KEY (`CustomerID`),
    UNIQUE INDEX `Email_UNIQUE` (`Email`),
    INDEX `fk_Customers_Genre_idx` (`GenreID`),
    CONSTRAINT `fk_Customers_Genre`
        FOREIGN KEY (`GenreID`)
        REFERENCES `Genre` (`GenreID`)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `Orders`;
CREATE TABLE IF NOT EXISTS `Orders` (
    `OrderID` INT NOT NULL AUTO_INCREMENT,
    `OrderDate` DATETIME NOT NULL,
    `PaymentMethod` ENUM('Credit Card', 'PayPal', 'Cash') NOT NULL,
    `OrderStatus` ENUM('Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled') NOT NULL,
    `CustomerID` INT NOT NULL,
    PRIMARY KEY (`OrderID`),
    INDEX `fk_Orders_Customers_idx` (`CustomerID`),
    CONSTRAINT `fk_Orders_Customers`
        FOREIGN KEY (`CustomerID`)
        REFERENCES `Customers` (`CustomerID`)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `Order_Line`;
CREATE TABLE IF NOT EXISTS `Order_Line` (
    `OrderLineID` INT NOT NULL AUTO_INCREMENT,
    `OrderID` INT NOT NULL,
    `AlbumID` INT NOT NULL,
    `Quantity` INT NOT NULL CHECK (Quantity > 0),
    `UnitPrice` DECIMAL(10,2) NOT NULL CHECK (UnitPrice > 0),
    PRIMARY KEY (`OrderLineID`),
    INDEX `fk_OLA_Order_idx` (`OrderID`),
    INDEX `fk_OLA_Album_idx` (`AlbumID`),
    CONSTRAINT `fk_OLA_Order`
        FOREIGN KEY (`OrderID`)
        REFERENCES `Orders` (`OrderID`)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT `fk_OLA_Album`
        FOREIGN KEY (`AlbumID`)
        REFERENCES `Album` (`AlbumID`)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;


INSERT INTO `Genre` (`GenreName`, `Description`) VALUES
('Rock', 'A genre of music characterized by a strong beat and the use of aggressive vocals.'),
('Pop', 'A genre of popular music that originated in its modern form during the mid-1950s.'),
('Jazz', 'A music genre that originated in the late 19th and early 20th centuries in African American communities in New Orleans.'),
('Classical', 'A genre of music that includes a wide range of styles from the late 18th century to the present day.'),
('Hip Hop', 'A genre of music that originated in the 1970s as a form of musical expression by African Americans.'),
('Electronic', 'A genre of music that originated in the 1970s and 1980s as a form of electronic music.'),
('Country', 'A genre of music that originated in the Southern United States in the early 1920s.'),
('Blues', 'A music genre and musical form that originated in the Deep South of the United States around the 1870s.'),
('R&B', 'A music genre that originated in the 1940s and developed from jazz and blues.'),
('Metal', 'A genre of rock music that is characterized by aggressive sounds and heavy use of distortion.'),
('Psychedelic Rock / Jam Band', 'A genre of rock music that combines elements of psychedelic music and jam band music.'),
('Rock / Jam Band', 'A genre of rock music that is characterized by a strong rhythm and a focus on improvisation.'),
('Psychedelic Rock / Garage Rock', 'A genre of rock music that combines elements of psychedelic music and garage rock music.'),
('Alternative Rock', 'A genre of rock music that originated in the 1970s and is characterized by its departure from mainstream rock music.'),
('Garage Rock / Psychedelic', 'A genre of rock music that combines elements of garage rock music and psychedelic music.'),
('Psychedelic Rock', 'A genre of rock music that is characterized by its use of psychedelic drugs and its focus on improvisation.'),
('Rock / Jam', 'A genre of rock music that combines elements of rock music and jam band music.'),
('Progressive Rock', 'A genre of rock music that is characterized by its complexity and its focus on improvisation.'),
('Funk Rock', 'A genre of rock music that combines elements of funk music and rock music.');

INSERT INTO Record_Label (LabelName, FoundedYear, Country) VALUES
  ('Grateful Dead Records', 1973, 'USA'),
  ('JEMP Records', 2004, 'USA'),
  ('Flightless Records', 2008, 'Australia'),
  ('GUM Records', 2015, 'Australia'),
  ('Murlocs Music', 2014, 'Australia'),
  ('Modular Recordings', 2005, 'Australia'),
  ('Columbia Records', 1888, 'USA'),
  ('Harvest Records', 1969, 'UK'),
  ('Gordon Records', 2008, 'USA');

INSERT INTO Band (BandName, FoundedYear, GenreID, Country, RecordLabelID) VALUES
  ('Grateful Dead', 1965, 1, 'USA', 1),
  ('Phish', 1983, 11, 'USA', 2),
  ('King Gizzard & The Lizard Wizard', 2010, 12, 'Australia', 3),
  ('GUM', 2015, 13, 'Australia', 4),
  ('The Murlocs', 2014, 14, 'Australia', 5),
  ('Tame Impala', 2007, 15, 'Australia', 6),
  ('Trey Anastasio Band', 2001, 16, 'USA', 7),
  ('Pink Floyd', 1965, 17, 'UK', 8),
  ('Mike Gordon Band', 2008, 18, 'USA', 9);

INSERT INTO Album (Title, ReleaseDate, Price, Format, BandID) VALUES
  ('American Beauty', '1970-02-22', 14.99, 'Vinyl', 1),
  ('Workingman''s Dead', '1970-06-27', 15.99, 'Vinyl', 1),
  ('Europe ''72', '1972-11-01', 16.99, 'CD', 1),
  ('Wake of the Flood', '1973-02-07', 17.99, 'Vinyl', 1),
  ('Terrapin Station', '1977-05-02', 18.99, 'CD', 1),
  ('Junta', '1989-09-01', 12.99, 'CD', 2),
  ('Lawn Boy', '1990-08-01', 13.49, 'CD', 2),
  ('A Picture of Nectar', '1992-10-20', 13.99, 'CD', 2),
  ('Hoist', '1994-08-01', 14.49, 'CD', 2),
  ('Billy Breathes', '1996-10-15', 15.49, 'CD', 2),
  ('12 Bar Bruise', '2012-03-01', 11.99, 'Digital', 3),
  ('I''m In Your Mind Fuzz', '2014-04-15', 12.99, 'Digital', 3),
  ('Nonagon Infinity', '2016-04-29', 15.99, 'Digital', 3),
  ('Flying Microtonal Banana', '2017-02-24', 16.99, 'CD', 3),
  ('Infest the Rats'' Nest', '2019-06-21', 17.99, 'Vinyl', 3),
  ('First Bite', '2015-11-01', 11.99, 'Digital', 4),
  ('Chewing the Fat', '2016-05-15', 12.49, 'CD', 4),
  ('Sticky Sweet', '2017-07-20', 13.49, 'Digital', 4),
  ('Resin Dreams', '2018-09-10', 14.49, 'Vinyl', 4),
  ('Sapling', '2019-12-01', 15.49, 'Digital', 4),
  ('Murlocs Unleashed', '2018-03-01', 10.99, 'Vinyl', 5),
  ('Deep Sea Echoes', '2019-04-10', 11.49, 'Digital', 5),
  ('Coastal Drift', '2020-05-05', 12.49, 'CD', 5),
  ('Tidal Grooves', '2021-06-15', 13.49, 'Digital', 5),
  ('Shoreline Dreams', '2022-07-20', 14.49, 'Vinyl', 5),
  ('Tame Impala (EP)', '2008-10-01', 9.99, 'Digital', 6),
  ('Innerspeaker', '2010-05-21', 13.99, 'CD', 6),
  ('Lonerism', '2012-10-05', 14.99, 'CD', 6),
  ('Currents', '2015-07-17', 16.99, 'CD', 6),
  ('The Slow Rush', '2020-02-14', 18.99, 'Vinyl', 6),
  ('Traveler', '2012-05-14', 12.49, 'Digital', 7),
  ('Paper Wheels', '2015-09-01', 13.99, 'CD', 7),
  ('Psychedelic Pulse', '2017-03-10', 14.99, 'Digital', 7),
  ('Jam Sessions', '2019-11-20', 15.99, 'CD', 7),
  ('Acoustic Vibes', '2021-08-25', 16.99, 'Digital', 7),
  ('The Piper at the Gates of Dawn', '1967-08-05', 17.99, 'Vinyl', 8),
  ('The Dark Side of the Moon', '1973-03-01', 18.99, 'Vinyl', 8),
  ('Wish You Were Here', '1975-09-12', 19.99, 'CD', 8),
  ('Animals', '1977-01-23', 18.49, 'CD', 8),
  ('The Wall', '1979-11-30', 20.99, 'Vinyl', 8),
  ('Inside and Out', '1998-03-10', 11.99, 'CD', 9),
  ('Tales from the Basement', '2000-07-15', 12.49, 'CD', 9),
  ('A Different Groove', '2003-09-20', 13.49, 'Digital', 9),
  ('Rhythm of Life', '2006-05-05', 14.49, 'CD', 9),
  ('Bass Odyssey', '2009-12-01', 15.49, 'Digital', 9);

INSERT INTO Customers (FirstName, LastName, Email, Phone, BirthDate, LoyaltyPoints, GenreID) VALUES
  ('John', 'Doe', 'john.doe@email.com', '908-420-2626', '1990-05-15', 100, 1),
  ('Jane', 'Smith', 'jane.smith@email.com', '212-555-1234', '1985-08-22', 50, 3),
  ('Bob', 'Johnson', 'bob.johnson@email.com', '718-333-4567', '1978-03-10', 75, 7),
  ('Alice', 'Williams', 'alice.williams@email.com', '646-777-8901', '1995-11-30', 25, 2),
  ('Charlie', 'Brown', 'charlie.brown@email.com', '917-222-3456', '1982-07-18', 150, 4);

INSERT INTO Orders (OrderDate, PaymentMethod, OrderStatus, CustomerID) VALUES
  ('2025-03-15 10:00:00', 'Credit Card', 'Shipped', 1),
  ('2025-03-16 11:30:00', 'PayPal', 'Processing', 2),
  ('2025-03-17 14:45:00', 'Credit Card', 'Delivered', 3);

INSERT INTO Order_Line (OrderID, AlbumID, Quantity, UnitPrice) VALUES
  (1, 1, 1, 14.99),
  (2, 29, 1, 18.99),
  (2, 38, 2, 18.49),
  (3, 8, 1, 13.99);


DROP FUNCTION IF EXISTS CalculateOrderTotal;
CREATE FUNCTION CalculateOrderTotal(order_id INT) 
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE total DECIMAL(10,2);
    
    SELECT SUM(ol.Quantity * ol.UnitPrice)
    INTO total
    FROM Order_Line ol
    WHERE ol.OrderID = order_id;
    
    RETURN COALESCE(total, 0);
END;

DROP PROCEDURE IF EXISTS sp_remove_loyalty_points;
CREATE PROCEDURE sp_remove_loyalty_points(
    IN p_order_id INT,
    OUT p_success BOOLEAN,
    OUT p_message VARCHAR(255)
)
sp_remove_loyalty_points: BEGIN
    DECLARE customer_id INT;
    DECLARE order_total DECIMAL(10,2);
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        GET DIAGNOSTICS CONDITION 1
        @sqlstate = RETURNED_SQLSTATE, @errno = MYSQL_ERRNO, @text = MESSAGE_TEXT;
        SET p_success = FALSE;
        SET p_message = CONCAT('Error: ', @sqlstate, ' - ', @text);
        ROLLBACK;
    END;

    START TRANSACTION;

    SELECT CustomerID INTO customer_id
    FROM Orders
    WHERE OrderID = p_order_id
    FOR UPDATE;

    IF customer_id IS NULL THEN
        SET p_success = FALSE;
        SET p_message = 'Order not found';
        ROLLBACK;
        LEAVE sp_remove_loyalty_points;
    END IF;

    SET order_total = CalculateOrderTotal(p_order_id);

    UPDATE Customers
    SET LoyaltyPoints = LoyaltyPoints - FLOOR(order_total)
    WHERE CustomerID = customer_id;

    SET p_success = TRUE;
    SET p_message = 'Loyalty points removed successfully';
    COMMIT;
END sp_remove_loyalty_points;

DROP TRIGGER IF EXISTS UpdateLoyaltyPoints;
CREATE TRIGGER UpdateLoyaltyPoints
AFTER UPDATE ON Orders
FOR EACH ROW
BEGIN
    IF NEW.OrderStatus = 'Processing' AND OLD.OrderStatus = 'Pending' THEN
        SET @order_total = CalculateOrderTotal(NEW.OrderID);
        
        UPDATE Customers c
        SET c.LoyaltyPoints = c.LoyaltyPoints + FLOOR(@order_total)
        WHERE c.CustomerID = NEW.CustomerID;
    END IF;
END;

DROP VIEW IF EXISTS vw_customers;
CREATE VIEW vw_customers AS
SELECT 
    c.CustomerID,
    CONCAT(c.FirstName, ' ', c.LastName) as Name,
    c.Email,
    c.Phone,
    DATE_FORMAT(c.BirthDate, '%Y-%m-%d') as BirthDate,
    c.LoyaltyPoints,
    g.GenreName as PreferredGenre,
    (SELECT COUNT(DISTINCT OrderID) FROM Orders o WHERE o.CustomerID = c.CustomerID) as TotalOrders,
    SUM(ol.Quantity * ol.UnitPrice) as TotalSpent
FROM Customers c
LEFT JOIN Genre g ON c.GenreID = g.GenreID
LEFT JOIN Orders o ON c.CustomerID = o.CustomerID
LEFT JOIN Order_Line ol ON o.OrderID = ol.OrderID
GROUP BY c.CustomerID, c.FirstName, c.LastName, c.Email, c.Phone, c.BirthDate, c.LoyaltyPoints, g.GenreName;

DROP VIEW IF EXISTS vw_bands;
CREATE VIEW vw_bands AS
SELECT 
    b.BandID,
    b.BandName,
    b.FoundedYear,
    g.GenreName as PrimaryGenre,
    b.Country,
    rl.LabelName as RecordLabel,
    (SELECT COUNT(*) FROM Album a WHERE a.BandID = b.BandID) as AlbumCount
FROM Band b
LEFT JOIN Record_Label rl ON b.RecordLabelID = rl.RecordLabelID
LEFT JOIN Genre g ON b.GenreID = g.GenreID
GROUP BY b.BandID, b.BandName, b.FoundedYear, g.GenreName, b.Country, rl.LabelName;

DROP VIEW IF EXISTS vw_albums;
CREATE VIEW vw_albums AS
SELECT 
    a.AlbumID,
    a.Title,
    DATE_FORMAT(a.ReleaseDate, '%Y-%m-%d') as ReleaseDate,
    a.Price,
    a.Format,
    b.BandName,
    g.GenreName as PrimaryGenre,
    COALESCE(COUNT(DISTINCT ol.OrderLineID), 0) as TimesOrdered,
    COALESCE(SUM(ol.Quantity), 0) as TotalQuantitySold
FROM Album a
JOIN Band b ON a.BandID = b.BandID
LEFT JOIN Genre g ON b.GenreID = g.GenreID
LEFT JOIN Order_Line ol ON a.AlbumID = ol.AlbumID
GROUP BY a.AlbumID, a.Title, a.ReleaseDate, a.Price, a.Format, b.BandName, g.GenreName;

DROP VIEW IF EXISTS vw_sales_by_genre;
CREATE VIEW vw_sales_by_genre AS
SELECT 
    g.GenreName,
    COUNT(DISTINCT o.OrderID) as TotalOrders,
    SUM(ol.Quantity) as TotalUnitsSold,
    SUM(ol.Quantity * ol.UnitPrice) as TotalRevenue,
    ROUND(AVG(ol.UnitPrice), 2) as AveragePrice
FROM Genre g
LEFT JOIN Band b ON g.GenreID = b.GenreID
LEFT JOIN Album a ON b.BandID = a.BandID
LEFT JOIN Order_Line ol ON a.AlbumID = ol.AlbumID
LEFT JOIN Orders o ON ol.OrderID = o.OrderID
GROUP BY g.GenreName
ORDER BY TotalRevenue DESC;

DROP VIEW IF EXISTS vw_customer_purchase_history;
CREATE VIEW vw_customer_purchase_history AS
SELECT 
    c.CustomerID,
    CONCAT(c.FirstName, ' ', c.LastName) as CustomerName,
    g.GenreName as PreferredGenre,
    COUNT(DISTINCT o.OrderID) as TotalOrders,
    SUM(ol.Quantity) as TotalItemsPurchased,
    SUM(ol.Quantity * ol.UnitPrice) as TotalSpent,
    MAX(o.OrderDate) as LastPurchaseDate,
    DATEDIFF(CURRENT_DATE, MAX(o.OrderDate)) as DaysSinceLastPurchase
FROM Customers c
LEFT JOIN Genre g ON c.GenreID = g.GenreID
LEFT JOIN Orders o ON c.CustomerID = o.CustomerID
LEFT JOIN Order_Line ol ON o.OrderID = ol.OrderID
GROUP BY c.CustomerID, c.FirstName, c.LastName, g.GenreName
ORDER BY TotalSpent DESC;

DROP VIEW IF EXISTS vw_band_performance;
CREATE VIEW vw_band_performance AS
SELECT 
    b.BandID,
    b.BandName,
    g.GenreName as PrimaryGenre,
    rl.LabelName as RecordLabel,
    COUNT(DISTINCT a.AlbumID) as TotalAlbums,
    COUNT(DISTINCT ol.OrderLineID) as TotalSales,
    SUM(ol.Quantity) as TotalUnitsSold,
    SUM(ol.Quantity * ol.UnitPrice) as TotalRevenue,
    AVG(ol.UnitPrice) as AveragePrice
FROM Band b
LEFT JOIN Record_Label rl ON b.RecordLabelID = rl.RecordLabelID
LEFT JOIN Album a ON b.BandID = a.BandID
LEFT JOIN Order_Line ol ON a.AlbumID = ol.AlbumID
LEFT JOIN Genre g ON b.GenreID = g.GenreID
GROUP BY b.BandID, b.BandName, g.GenreName, rl.LabelName
ORDER BY TotalRevenue DESC;

DROP VIEW IF EXISTS vw_inventory_analysis;
CREATE VIEW vw_inventory_analysis AS
SELECT 
    a.AlbumID,
    a.Title,
    b.BandName,
    a.Format,
    a.Price,
    COUNT(ol.OrderLineID) as TimesOrdered,
    SUM(ol.Quantity) as TotalSold,
    DATEDIFF(CURRENT_DATE, a.ReleaseDate) as DaysSinceRelease,
    CASE 
        WHEN COUNT(ol.OrderLineID) = 0 THEN 'New'
        WHEN DATEDIFF(CURRENT_DATE, MAX(o.OrderDate)) > 90 THEN 'Slow Moving'
        ELSE 'Active'
    END as InventoryStatus
FROM Album a
JOIN Band b ON a.BandID = b.BandID
LEFT JOIN Order_Line ol ON a.AlbumID = ol.AlbumID
LEFT JOIN Orders o ON ol.OrderID = o.OrderID
GROUP BY a.AlbumID, a.Title, b.BandName, a.Format, a.Price, a.ReleaseDate
ORDER BY TotalSold DESC;

DROP VIEW IF EXISTS vw_order_details;
CREATE VIEW vw_order_details AS
SELECT 
    o.OrderID,
    CONCAT(c.FirstName, ' ', c.LastName) as Customer,
    o.OrderDate,
    o.PaymentMethod,
    o.OrderStatus,
    CalculateOrderTotal(o.OrderID) as TotalAmount
FROM Orders o
JOIN Customers c ON o.CustomerID = c.CustomerID
ORDER BY o.OrderDate DESC;

DROP VIEW IF EXISTS vw_order_items;
CREATE VIEW vw_order_items AS
SELECT 
    ol.OrderID,
    a.Title,
    ol.Quantity,
    ol.UnitPrice,
    (ol.Quantity * ol.UnitPrice) as ItemTotal
FROM Order_Line ol
JOIN Album a ON ol.AlbumID = a.AlbumID
ORDER BY ol.OrderID;

DROP VIEW IF EXISTS vw_genres;
CREATE VIEW vw_genres AS
SELECT 
    g.GenreID,
    g.GenreName,
    g.Description,
    (SELECT COUNT(*) FROM Band b WHERE b.GenreID = g.GenreID) as BandCount,
    (SELECT COUNT(*) FROM Customers c WHERE c.GenreID = g.GenreID) as CustomerCount
FROM Genre g;

DROP VIEW IF EXISTS vw_record_labels;
CREATE VIEW vw_record_labels AS
SELECT 
    rl.RecordLabelID,
    rl.LabelName,
    rl.FoundedYear,
    rl.Country,
    (SELECT COUNT(*) FROM Band b WHERE b.RecordLabelID = rl.RecordLabelID) as BandCount
FROM Record_Label rl;

CREATE VIEW vw_order_summary AS
SELECT 
    o.OrderID,
    o.OrderDate,
    o.PaymentMethod,
    o.OrderStatus,
    c.CustomerID,
    CONCAT(c.FirstName, ' ', c.LastName) AS CustomerName,
    CalculateOrderTotal(o.OrderID) AS TotalAmount
FROM Orders o
JOIN Customers c ON o.CustomerID = c.CustomerID;

