package com.evanalytics.dto;

import java.math.BigDecimal;

public record KpiSummary(
        long customers,
        long products,
        long completedOrders,
        BigDecimal revenue,
        BigDecimal averageOrderValue,
        BigDecimal averageChurnRisk
) { }
