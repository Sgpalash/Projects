ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '123456789';
FLUSH PRIVILEGES;

USE restaurantDB
INSERT INTO Menu (name, price, restaurant) VALUES
('Margherita Pizza', 299.00, 'Pizza Palace'),
('Cheeseburger', 199.00, 'Burger House'),
('Pasta Alfredo', 249.00, 'Italiano'),
('Veggie Wrap', 149.00, 'Healthy Bites');

SELECT * FROM Users; 
Show databases
SHOW tables;

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_type VARCHAR(20) NOT NULL,
    table_no INT NULL,
    address VARCHAR(255) NULL,
    phone VARCHAR(20) NULL,
    items JSON NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SELECT * FROM Orders

DESCRIBE orders;

DROP TABLE IF EXISTS orders;

CREATE TABLE orders (
  order_id INT AUTO_INCREMENT PRIMARY KEY,
  order_type VARCHAR(20),
  table_no INT NULL,
  address VARCHAR(255) NULL,
  phone VARCHAR(20) NULL,
  items JSON NOT NULL,
  total DECIMAL(10,2) NOT NULL,
  date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

