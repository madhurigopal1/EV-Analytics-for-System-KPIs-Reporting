package com.evanalytics.service;

import com.evanalytics.dto.KpiSummary;
import com.evanalytics.dto.ProductKpi;
import com.evanalytics.dto.SegmentKpi;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;
import java.math.BigDecimal;
import java.util.List;

@Service
public class KpiService {
    private final JdbcTemplate jdbc;
    public KpiService(JdbcTemplate jdbc) { this.jdbc = jdbc; }

    public KpiSummary summary() {
        Long customers = jdbc.queryForObject("SELECT COUNT(*) FROM customers", Long.class);
        Long products = jdbc.queryForObject("SELECT COUNT(*) FROM products", Long.class);
        Long orders = jdbc.queryForObject("SELECT COUNT(*) FROM sales_transactions WHERE status='Completed'", Long.class);
        BigDecimal revenue = jdbc.queryForObject("SELECT COALESCE(SUM(total_amount),0) FROM sales_transactions WHERE status='Completed'", BigDecimal.class);
        BigDecimal avgOrder = jdbc.queryForObject("SELECT COALESCE(AVG(total_amount),0) FROM sales_transactions WHERE status='Completed'", BigDecimal.class);
        BigDecimal churn = jdbc.queryForObject("SELECT COALESCE(AVG(churn_risk),0) FROM customers", BigDecimal.class);
        return new KpiSummary(customers, products, orders, revenue, avgOrder, churn);
    }

    public List<SegmentKpi> segments() {
        return jdbc.query("SELECT segment, COUNT(*) customer_count, AVG(annual_income) average_income, AVG(purchase_frequency) average_purchase_frequency, AVG(churn_risk) average_churn_risk FROM customers GROUP BY segment ORDER BY customer_count DESC",
                (rs, row) -> new SegmentKpi(rs.getString("segment"), rs.getLong("customer_count"), rs.getBigDecimal("average_income"), rs.getBigDecimal("average_purchase_frequency"), rs.getBigDecimal("average_churn_risk")));
    }

    public List<ProductKpi> products() {
        return jdbc.query("SELECT category, COUNT(*) product_count, AVG(price) average_price, AVG(efficiency_score) average_efficiency, SUM(stock_quantity) available_stock FROM products GROUP BY category ORDER BY product_count DESC",
                (rs, row) -> new ProductKpi(rs.getString("category"), rs.getLong("product_count"), rs.getBigDecimal("average_price"), rs.getBigDecimal("average_efficiency"), rs.getLong("available_stock")));
    }

    public String aggregateContext() {
        KpiSummary s = summary();
        List<SegmentKpi> bySegment = segments();
        List<ProductKpi> byProduct = products();
        return "Aggregate KPIs only. Summary=" + s + "; customer segments=" + bySegment + "; product categories=" + byProduct;
    }
}
