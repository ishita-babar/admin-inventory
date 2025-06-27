-- Smart Inventory Management Database Schema

-- Create database
CREATE DATABASE IF NOT EXISTS inventory_dashboard;
\c inventory_dashboard;

-- Categories table
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    sku VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    category_id INTEGER REFERENCES categories(id),
    price DECIMAL(10,2) NOT NULL,
    inventory_count INTEGER DEFAULT 0,
    min_stock_level INTEGER DEFAULT 10,
    max_stock_level INTEGER DEFAULT 100,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sales table
CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    revenue DECIMAL(10,2) NOT NULL,
    sale_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Reviews table
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    review_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Returns table
CREATE TABLE returns (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    return_reason VARCHAR(200),
    return_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert dummy categories
INSERT INTO categories (name, description) VALUES
('Electronics', 'Electronic devices and accessories'),
('Clothing', 'Apparel and fashion items'),
('Home & Garden', 'Home improvement and garden supplies'),
('Sports', 'Sports equipment and accessories'),
('Books', 'Books and educational materials');

-- Insert dummy products
INSERT INTO products (sku, name, description, category_id, price, inventory_count, min_stock_level, max_stock_level) VALUES
('ELE-001', 'Wireless Headphones', 'Premium noise-cancelling wireless headphones', 1, 199.99, 45, 20, 100),
('ELE-002', 'Smartphone', 'Latest smartphone with advanced features', 1, 899.99, 12, 15, 50),
('ELE-003', 'Laptop', 'High-performance laptop for professionals', 1, 1299.99, 8, 10, 30),
('CLO-001', 'Cotton T-Shirt', 'Comfortable cotton t-shirt in various colors', 2, 24.99, 150, 50, 200),
('CLO-002', 'Denim Jeans', 'Classic denim jeans for everyday wear', 2, 79.99, 85, 30, 120),
('CLO-003', 'Running Shoes', 'Professional running shoes with cushioning', 2, 129.99, 32, 25, 80),
('HOM-001', 'Garden Hose', 'Durable garden hose 50ft length', 3, 39.99, 67, 20, 100),
('HOM-002', 'Kitchen Blender', 'High-speed kitchen blender for smoothies', 3, 89.99, 23, 15, 60),
('HOM-003', 'LED Light Bulbs', 'Energy-efficient LED light bulbs pack of 4', 3, 19.99, 120, 40, 150),
('SPO-001', 'Yoga Mat', 'Non-slip yoga mat for home workouts', 4, 34.99, 78, 30, 100),
('SPO-002', 'Basketball', 'Official size basketball for indoor/outdoor use', 4, 29.99, 45, 20, 80),
('SPO-003', 'Tennis Racket', 'Professional tennis racket with case', 4, 159.99, 18, 10, 40),
('BOO-001', 'Programming Guide', 'Complete guide to modern programming', 5, 49.99, 95, 30, 120),
('BOO-002', 'Cookbook', 'Collection of international recipes', 5, 34.99, 62, 25, 80),
('BOO-003', 'Fitness Manual', 'Comprehensive fitness and nutrition guide', 5, 39.99, 41, 20, 70);

-- Insert dummy sales data (last 6 months)
INSERT INTO sales (product_id, quantity, revenue, sale_date) VALUES
-- Electronics
(1, 15, 2999.85, CURRENT_DATE - INTERVAL '1 month'),
(1, 12, 2399.88, CURRENT_DATE - INTERVAL '2 months'),
(1, 18, 3599.82, CURRENT_DATE - INTERVAL '3 months'),
(2, 8, 7199.92, CURRENT_DATE - INTERVAL '1 month'),
(2, 6, 5399.94, CURRENT_DATE - INTERVAL '2 months'),
(2, 10, 8999.90, CURRENT_DATE - INTERVAL '3 months'),
(3, 5, 6499.95, CURRENT_DATE - INTERVAL '1 month'),
(3, 7, 9099.93, CURRENT_DATE - INTERVAL '2 months'),
(3, 4, 5199.96, CURRENT_DATE - INTERVAL '3 months'),

-- Clothing
(4, 45, 1124.55, CURRENT_DATE - INTERVAL '1 month'),
(4, 38, 949.62, CURRENT_DATE - INTERVAL '2 months'),
(4, 52, 1299.48, CURRENT_DATE - INTERVAL '3 months'),
(5, 22, 1759.78, CURRENT_DATE - INTERVAL '1 month'),
(5, 18, 1439.82, CURRENT_DATE - INTERVAL '2 months'),
(5, 25, 1999.75, CURRENT_DATE - INTERVAL '3 months'),
(6, 15, 1949.85, CURRENT_DATE - INTERVAL '1 month'),
(6, 12, 1559.88, CURRENT_DATE - INTERVAL '2 months'),
(6, 20, 2599.80, CURRENT_DATE - INTERVAL '3 months'),

-- Home & Garden
(7, 28, 1119.72, CURRENT_DATE - INTERVAL '1 month'),
(7, 25, 999.75, CURRENT_DATE - INTERVAL '2 months'),
(7, 32, 1279.68, CURRENT_DATE - INTERVAL '3 months'),
(8, 12, 1079.88, CURRENT_DATE - INTERVAL '1 month'),
(8, 10, 899.90, CURRENT_DATE - INTERVAL '2 months'),
(8, 15, 1349.85, CURRENT_DATE - INTERVAL '3 months'),
(9, 35, 699.65, CURRENT_DATE - INTERVAL '1 month'),
(9, 42, 839.58, CURRENT_DATE - INTERVAL '2 months'),
(9, 38, 759.62, CURRENT_DATE - INTERVAL '3 months'),

-- Sports
(10, 25, 874.75, CURRENT_DATE - INTERVAL '1 month'),
(10, 22, 769.78, CURRENT_DATE - INTERVAL '2 months'),
(10, 30, 1049.70, CURRENT_DATE - INTERVAL '3 months'),
(11, 18, 539.82, CURRENT_DATE - INTERVAL '1 month'),
(11, 15, 449.85, CURRENT_DATE - INTERVAL '2 months'),
(11, 22, 659.78, CURRENT_DATE - INTERVAL '3 months'),
(12, 8, 1279.92, CURRENT_DATE - INTERVAL '1 month'),
(12, 6, 959.94, CURRENT_DATE - INTERVAL '2 months'),
(12, 10, 1599.90, CURRENT_DATE - INTERVAL '3 months'),

-- Books
(13, 30, 1499.70, CURRENT_DATE - INTERVAL '1 month'),
(13, 25, 1249.75, CURRENT_DATE - INTERVAL '2 months'),
(13, 35, 1749.65, CURRENT_DATE - INTERVAL '3 months'),
(14, 20, 699.80, CURRENT_DATE - INTERVAL '1 month'),
(14, 18, 629.82, CURRENT_DATE - INTERVAL '2 months'),
(14, 25, 874.75, CURRENT_DATE - INTERVAL '3 months'),
(15, 15, 599.85, CURRENT_DATE - INTERVAL '1 month'),
(15, 12, 479.88, CURRENT_DATE - INTERVAL '2 months'),
(15, 18, 719.82, CURRENT_DATE - INTERVAL '3 months');

-- Insert dummy reviews
INSERT INTO reviews (product_id, rating, comment, review_date) VALUES
(1, 5, 'Excellent sound quality!', CURRENT_DATE - INTERVAL '5 days'),
(1, 4, 'Great headphones, good battery life', CURRENT_DATE - INTERVAL '10 days'),
(1, 5, 'Perfect for work calls', CURRENT_DATE - INTERVAL '15 days'),
(2, 4, 'Fast phone, good camera', CURRENT_DATE - INTERVAL '7 days'),
(2, 3, 'Battery could be better', CURRENT_DATE - INTERVAL '12 days'),
(2, 5, 'Amazing performance', CURRENT_DATE - INTERVAL '20 days'),
(3, 5, 'Perfect for development work', CURRENT_DATE - INTERVAL '8 days'),
(3, 4, 'Good laptop, runs smoothly', CURRENT_DATE - INTERVAL '14 days'),
(3, 5, 'Excellent build quality', CURRENT_DATE - INTERVAL '25 days'),
(4, 4, 'Comfortable and durable', CURRENT_DATE - INTERVAL '6 days'),
(4, 5, 'Great fit and feel', CURRENT_DATE - INTERVAL '11 days'),
(4, 3, 'Slightly expensive for basic t-shirt', CURRENT_DATE - INTERVAL '18 days'),
(5, 5, 'Perfect fit and quality', CURRENT_DATE - INTERVAL '9 days'),
(5, 4, 'Good jeans, comfortable', CURRENT_DATE - INTERVAL '16 days'),
(5, 5, 'Excellent durability', CURRENT_DATE - INTERVAL '22 days');

-- Insert dummy returns
INSERT INTO returns (product_id, quantity, return_reason, return_date) VALUES
(1, 2, 'Defective unit', CURRENT_DATE - INTERVAL '3 days'),
(1, 1, 'Wrong color ordered', CURRENT_DATE - INTERVAL '8 days'),
(2, 1, 'Screen damage', CURRENT_DATE - INTERVAL '5 days'),
(2, 1, 'Not as expected', CURRENT_DATE - INTERVAL '12 days'),
(3, 1, 'Performance issues', CURRENT_DATE - INTERVAL '7 days'),
(4, 3, 'Size too small', CURRENT_DATE - INTERVAL '4 days'),
(4, 2, 'Color faded after wash', CURRENT_DATE - INTERVAL '10 days'),
(5, 1, 'Wrong size', CURRENT_DATE - INTERVAL '6 days'),
(6, 1, 'Comfort issues', CURRENT_DATE - INTERVAL '9 days'),
(7, 2, 'Leaking hose', CURRENT_DATE - INTERVAL '5 days'),
(8, 1, 'Blade malfunction', CURRENT_DATE - INTERVAL '11 days'),
(9, 4, 'Bulbs not working', CURRENT_DATE - INTERVAL '7 days'),
(10, 1, 'Mat too thin', CURRENT_DATE - INTERVAL '8 days'),
(11, 1, 'Ball deflated', CURRENT_DATE - INTERVAL '6 days'),
(12, 1, 'Racket string broke', CURRENT_DATE - INTERVAL '10 days');

-- Create indexes for better performance
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_sales_product_date ON sales(product_id, sale_date);
CREATE INDEX idx_reviews_product_date ON reviews(product_id, review_date);
CREATE INDEX idx_returns_product_date ON returns(product_id, return_date);

-- Create view for product analytics
CREATE VIEW product_analytics AS
SELECT 
    p.id,
    p.sku,
    p.name,
    p.category_id,
    c.name as category_name,
    p.price,
    p.inventory_count,
    p.min_stock_level,
    p.max_stock_level,
    COALESCE(SUM(s.quantity), 0) as total_sales_quantity,
    COALESCE(SUM(s.revenue), 0) as total_revenue,
    COALESCE(AVG(r.rating), 0) as avg_rating,
    COALESCE(COUNT(r.id), 0) as review_count,
    COALESCE(SUM(ret.quantity), 0) as total_returns,
    CASE 
        WHEN p.inventory_count <= p.min_stock_level THEN 'Low Stock'
        WHEN p.inventory_count >= p.max_stock_level THEN 'Overstock'
        ELSE 'In Stock'
    END as inventory_status
FROM products p
LEFT JOIN categories c ON p.category_id = c.id
LEFT JOIN sales s ON p.id = s.product_id AND s.sale_date >= CURRENT_DATE - INTERVAL '30 days'
LEFT JOIN reviews r ON p.id = r.product_id AND r.review_date >= CURRENT_DATE - INTERVAL '60 days'
LEFT JOIN returns ret ON p.id = ret.product_id AND ret.return_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY p.id, p.sku, p.name, p.category_id, c.name, p.price, p.inventory_count, p.min_stock_level, p.max_stock_level; 