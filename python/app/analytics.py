from sqlalchemy import create_engine, text
import os


def get_engine():
    return create_engine(os.environ["DATABASE_URL"], pool_pre_ping=True, pool_recycle=1800)


def summary():
    with get_engine().connect() as conn:
        return conn.execute(text("""
            SELECT (SELECT COUNT(*) FROM customers) AS customers,
                   (SELECT COUNT(*) FROM products) AS products,
                   (SELECT COUNT(*) FROM sales_transactions WHERE status='Completed') AS completed_orders,
                   (SELECT COALESCE(SUM(total_amount),0) FROM sales_transactions WHERE status='Completed') AS revenue,
                   (SELECT COALESCE(AVG(churn_risk),0) FROM customers) AS average_churn_risk
        """)).mappings().one()._asdict()


def segment_kpis():
    with get_engine().connect() as conn:
        return [dict(row) for row in conn.execute(text("""
            SELECT segment, COUNT(*) customer_count, ROUND(AVG(annual_income),2) average_income,
                   ROUND(AVG(purchase_frequency),2) average_purchase_frequency,
                   ROUND(AVG(churn_risk),4) average_churn_risk
            FROM customers GROUP BY segment ORDER BY customer_count DESC
        """ )).mappings().all()]


def product_kpis():
    with get_engine().connect() as conn:
        return [dict(row) for row in conn.execute(text("""
            SELECT category, COUNT(*) product_count, ROUND(AVG(price),2) average_price,
                   ROUND(AVG(efficiency_score),2) average_efficiency, SUM(stock_quantity) available_stock
            FROM products GROUP BY category ORDER BY product_count DESC
        """)).mappings().all()]
