package com.evanalytics.dto;

import java.math.BigDecimal;

public record SegmentKpi(String segment, long customerCount, BigDecimal averageIncome,
                         BigDecimal averagePurchaseFrequency, BigDecimal averageChurnRisk) { }
