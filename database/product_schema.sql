-- product_schema.sql

CREATE TABLE IF NOT EXISTS products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    description TEXT,
    unit_price DECIMAL(10, 2) NOT NULL,
    store_id INT REFERENCES stores(store_id) ON DELETE CASCADE,
    available_quantity INT CHECK (available_quantity >= 0),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index to speed up product lookups
CREATE INDEX idx_products_name ON products(product_name);
