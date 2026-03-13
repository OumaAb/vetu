-- =============================================
-- CLOTHES RENTAL APP - DATABASE SETUP
-- Run this file in MySQL to create the database
-- mysql -u root -p < database.sql
-- =============================================

CREATE DATABASE IF NOT EXISTS clothes_rental;

CREATE USER IF NOT EXISTS 'rental_user'@'%' IDENTIFIED BY 'rental123';
GRANT ALL PRIVILEGES ON clothes_rental.* TO 'rental_user'@'%';
FLUSH PRIVILEGES;
USE clothes_rental;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('user', 'admin') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Clothes table
CREATE TABLE IF NOT EXISTS clothes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    category VARCHAR(50) NOT NULL,
    size VARCHAR(20) NOT NULL,
    price_per_day DECIMAL(10,2) NOT NULL,
    image_url VARCHAR(500),
    available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Rentals table
CREATE TABLE IF NOT EXISTS rentals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    cloth_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    status ENUM('pending', 'active', 'returned', 'cancelled') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (cloth_id) REFERENCES clothes(id)
);

-- Default admin user (password: admin123)
INSERT INTO users (name, email, password, role) VALUES
('Admin', 'admin@rental.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewJqzrqx6kGDUeGi', 'admin');

-- Sample clothes
INSERT INTO clothes (name, description, category, size, price_per_day, image_url, available) VALUES
('Elegant Black Dress', 'Perfect for evening events and galas', 'Dress', 'M', 25.00, 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400', TRUE),
('Classic Tuxedo', 'Timeless black tuxedo for formal occasions', 'Suit', 'L', 45.00, 'https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=400', TRUE),
('Summer Floral Dress', 'Light and breezy floral print dress', 'Dress', 'S', 15.00, 'https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=400', TRUE),
('Business Blazer', 'Professional navy blue blazer', 'Jacket', 'M', 20.00, 'https://images.unsplash.com/photo-1594938298603-c8148c4b4a74?w=400', TRUE),
('Cocktail Dress', 'Stylish red cocktail dress', 'Dress', 'S', 30.00, 'https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=400', TRUE),
('Casual Denim Jacket', 'Trendy oversized denim jacket', 'Jacket', 'L', 12.00, 'https://images.unsplash.com/photo-1551537482-f2075a1d41f2?w=400', TRUE);
