CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    contact_number VARCHAR(30),
    address TEXT,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Managers (
    manager_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE Brands (
    brand_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    status ENUM('active', 'inactive', 'old') DEFAULT 'active'
);

CREATE TABLE Products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL,
    category_id INT,
    brand_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('active', 'inactive') DEFAULT 'active',
    FOREIGN KEY (category_id) REFERENCES Categories(category_id),
    FOREIGN KEY (brand_id) REFERENCES Brands(brand_id)
);

CREATE TABLE ShippingInfo (
    shipping_info_id INT AUTO_INCREMENT PRIMARY KEY,
    tracking_number VARCHAR(50),
    carrier VARCHAR(100),
    shipping_date DATE,
    delivery_date DATE,
    status ENUM('pending', 'shipped', 'delivered', 'returned') DEFAULT 'pending'
);

CREATE TABLE Orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled', 'returned') NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    shipping_info_id INT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (shipping_info_id) REFERENCES ShippingInfo(shipping_info_id)
);

CREATE TABLE OrderDetails (
    order_detail_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

CREATE TABLE ShoppingCart (
    cart_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE CartItems (
    cart_item_id INT AUTO_INCREMENT PRIMARY KEY,
    cart_id INT,
    product_id INT,
    quantity INT NOT NULL,
    FOREIGN KEY (cart_id) REFERENCES ShoppingCart(cart_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

CREATE TABLE PurchaseHistory (
    history_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    order_id INT,
    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);

CREATE TABLE Comments (
    comment_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    user_id INT,
    comment TEXT NOT NULL,
    comment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('approved', 'inappropriate') DEFAULT 'approved',
    moderated_by INT,
    FOREIGN KEY (product_id) REFERENCES Products(product_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (moderated_by) REFERENCES Managers(manager_id)
);

CREATE TABLE Discounts (
    discount_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    discount_percentage DECIMAL(5, 2) NOT NULL,
    start_date DATE,
    end_date DATE
);

CREATE TABLE ProductDiscounts (
    product_discount_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    discount_id INT,
    FOREIGN KEY (product_id) REFERENCES Products(product_id),
    FOREIGN KEY (discount_id) REFERENCES Discounts(discount_id)
);
