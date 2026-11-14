CREATE DATABASE IF NOT EXISTS ev_analytics;
USE ev_analytics;

CREATE TABLE IF NOT EXISTS customers (
    id BIGINT NOT NULL PRIMARY KEY,
    customer_name VARCHAR(120) NOT NULL,
    segment VARCHAR(32) NOT NULL,
    city VARCHAR(80) NOT NULL,
    region VARCHAR(32) NOT NULL,
    age SMALLINT NOT NULL,
    annual_income DECIMAL(12,2) NOT NULL,
    purchase_frequency SMALLINT NOT NULL,
    tenure_months SMALLINT NOT NULL,
    churn_risk DECIMAL(5,4) NOT NULL,
    created_at DATETIME NOT NULL,
    INDEX idx_customers_segment (segment),
    INDEX idx_customers_region (region),
    INDEX idx_customers_churn (churn_risk)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS products (
    id BIGINT NOT NULL PRIMARY KEY,
    product_name VARCHAR(120) NOT NULL,
    category VARCHAR(40) NOT NULL,
    model_type VARCHAR(32) NOT NULL,
    battery_capacity_kwh DECIMAL(7,2) NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    efficiency_score DECIMAL(5,2) NOT NULL,
    stock_quantity INT NOT NULL,
    launch_date DATE NOT NULL,
    INDEX idx_products_category (category),
    INDEX idx_products_stock (stock_quantity)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS sales_transactions (
    id BIGINT NOT NULL PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    transaction_date DATETIME NOT NULL,
    quantity SMALLINT NOT NULL,
    unit_price DECIMAL(12,2) NOT NULL,
    total_amount DECIMAL(14,2) NOT NULL,
    sales_channel VARCHAR(32) NOT NULL,
    region VARCHAR(32) NOT NULL,
    status VARCHAR(16) NOT NULL,
    INDEX idx_sales_date (transaction_date),
    INDEX idx_sales_status_date (status, transaction_date),
    INDEX idx_sales_customer (customer_id),
    INDEX idx_sales_product (product_id),
    CONSTRAINT fk_sales_customer FOREIGN KEY (customer_id) REFERENCES customers(id),
    CONSTRAINT fk_sales_product FOREIGN KEY (product_id) REFERENCES products(id)
) ENGINE=InnoDB;
