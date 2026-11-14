import os
import random
from datetime import datetime, timedelta
from decimal import Decimal
from faker import Faker
from sqlalchemy import create_engine, text

fake = Faker()


def engine():
    return create_engine(os.environ["DATABASE_URL"], pool_pre_ping=True, pool_recycle=1800)


def generate_and_load(seed: int = 42):
    random.seed(seed)
    Faker.seed(seed)
    db = engine()
    with db.begin() as conn:
        existing = conn.execute(text("SELECT COUNT(*) FROM customers")).scalar_one()
        if existing > 0:
            return {"status": "skipped", "reason": "customers table is not empty", "customers": existing}

        regions = ["North", "South", "East", "West", "Central"]
        segments = ["Urban", "Suburban", "Rural"]
        categories = ["EV Sedan", "EV SUV", "Commercial EV"]
        batch = []
        now = datetime.utcnow()
        for i in range(1, 10001):
            churn = round(random.uniform(0.02, 0.40), 4)
            batch.append({"id": i, "customer_name": fake.name()[:120], "segment": random.choice(segments),
                          "city": fake.city()[:80], "region": random.choice(regions), "age": random.randint(21, 75),
                          "annual_income": round(random.uniform(35000, 180000), 2),
                          "purchase_frequency": random.randint(1, 12), "tenure_months": random.randint(1, 120),
                          "churn_risk": churn, "created_at": now - timedelta(days=random.randint(0, 2500))})
            if len(batch) == 1000:
                conn.execute(text("INSERT INTO customers (id,customer_name,segment,city,region,age,annual_income,purchase_frequency,tenure_months,churn_risk,created_at) VALUES (:id,:customer_name,:segment,:city,:region,:age,:annual_income,:purchase_frequency,:tenure_months,:churn_risk,:created_at)"), batch)
                batch.clear()
        if batch:
            conn.execute(text("INSERT INTO customers (id,customer_name,segment,city,region,age,annual_income,purchase_frequency,tenure_months,churn_risk,created_at) VALUES (:id,:customer_name,:segment,:city,:region,:age,:annual_income,:purchase_frequency,:tenure_months,:tenure_months,:churn_risk,:created_at)"), batch)

        batch = []
        for i in range(1, 10001):
            batch.append({"id": i, "product_name": f"EV Model {i:05d}", "category": random.choice(categories),
                          "model_type": random.choice(["Compact", "Premium", "Utility"]),
                          "battery_capacity_kwh": round(random.uniform(30, 120), 2),
                          "price": round(random.uniform(25000, 95000), 2),
                          "efficiency_score": round(random.uniform(60, 98), 2),
                          "stock_quantity": random.randint(0, 500),
                          "launch_date": (now - timedelta(days=random.randint(30, 2200))).date()})
            if len(batch) == 1000:
                conn.execute(text("INSERT INTO products (id,product_name,category,model_type,battery_capacity_kwh,price,efficiency_score,stock_quantity,launch_date) VALUES (:id,:product_name,:category,:model_type,:battery_capacity_kwh,:price,:efficiency_score,:stock_quantity,:launch_date)"), batch)
                batch.clear()
        if batch:
            conn.execute(text("INSERT INTO products (id,product_name,category,model_type,battery_capacity_kwh,price,efficiency_score,stock_quantity,launch_date) VALUES (:id,:product_name,:category,:model_type,:battery_capacity_kwh,:price,:efficiency_score,:stock_quantity,:launch_date)"), batch)

        # Moderate-sized transaction history supports useful revenue and order metrics.
        statuses = ["Completed", "Pending", "Cancelled"]
        channels = ["Online", "Dealer", "Fleet", "Direct"]
        batch = []
        for i in range(1, 50001):
            quantity = random.randint(1, 3)
            price = Decimal(str(round(random.uniform(25000, 95000), 2)))
            batch.append({"id": i, "customer_id": random.randint(1, 10000), "product_id": random.randint(1, 10000),
                          "transaction_date": now - timedelta(days=random.randint(0, 1800)), "quantity": quantity,
                          "unit_price": price, "total_amount": price * quantity, "sales_channel": random.choice(channels),
                          "region": random.choice(regions), "status": random.choices(statuses, weights=[80, 12, 8])[0]})
            if len(batch) == 1000:
                conn.execute(text("INSERT INTO sales_transactions (id,customer_id,product_id,transaction_date,quantity,unit_price,total_amount,sales_channel,region,status) VALUES (:id,:customer_id,:product_id,:transaction_date,:quantity,:unit_price,:total_amount,:sales_channel,:region,:status)"), batch)
                batch.clear()
        if batch:
            conn.execute(text("INSERT INTO sales_transactions (id,customer_id,product_id,transaction_date,quantity,unit_price,total_amount,sales_channel,region,status) VALUES (:id,:customer_id,:product_id,:transaction_date,:quantity,:unit_price,:total_amount,:sales_channel,:region,:status)"), batch)
    return {"status": "loaded", "customers": 10000, "products": 10000, "transactions": 50000}
