package com.evanalytics.dto;

import java.math.BigDecimal;

public record ProductKpi(String category, long productCount, BigDecimal averagePrice,
                         BigDecimal averageEfficiency, long availableStock) { }
