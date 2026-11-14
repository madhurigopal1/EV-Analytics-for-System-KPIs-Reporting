package com.evanalytics.controller;

import com.evanalytics.dto.KpiSummary;
import com.evanalytics.dto.ProductKpi;
import com.evanalytics.dto.SegmentKpi;
import com.evanalytics.service.KpiService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.List;

@RestController
@RequestMapping("/api/kpis")
public class KpiController {
    private final KpiService service;
    public KpiController(KpiService service) { this.service = service; }
    @GetMapping public KpiSummary summary() { return service.summary(); }
    @GetMapping("/segments") public List<SegmentKpi> segments() { return service.segments(); }
    @GetMapping("/products") public List<ProductKpi> products() { return service.products(); }
}
