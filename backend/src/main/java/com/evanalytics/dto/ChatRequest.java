package com.evanalytics.dto;

import jakarta.validation.constraints.NotBlank;

public record ChatRequest(@NotBlank String question) { }
