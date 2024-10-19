-- Create table for user information
CREATE TABLE IF NOT EXISTS users (
    userid SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULl,
    phone VARCHAR(12) UNIQUE, -- Optional
    address VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAT(255) NOT NULL
);

-- Create table for user lists
CREATE TABLE IF NOT EXISTS user_lists (
    list_id SERIAL PRIMARY KEY,
    userid serial REFERENCES users(userid),
    list_name VARCHAR(255) UNIQUE NOT NULL,
    item VARCHAR(50) NOT NULL,
    item_quantity INT NOT NULL,
    item_cost REAL(2)
);