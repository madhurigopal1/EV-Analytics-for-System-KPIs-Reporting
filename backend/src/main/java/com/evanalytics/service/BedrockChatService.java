package com.evanalytics.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import software.amazon.awssdk.core.SdkBytes;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.bedrockruntime.BedrockRuntimeClient;
import software.amazon.awssdk.services.bedrockruntime.model.InvokeModelRequest;
import java.util.Map;

@Service
public class BedrockChatService {
    private final KpiService kpis;
    private final ObjectMapper mapper = new ObjectMapper();
    private final String region;
    private final String modelId;

    public BedrockChatService(KpiService kpis, @Value("${aws.region}") String region,
                              @Value("${aws.bedrock.model-id:}") String modelId) {
        this.kpis = kpis; this.region = region; this.modelId = modelId;
    }

    public String answer(String question) {
        String context = kpis.aggregateContext();
        if (modelId == null || modelId.isBlank()) return localAnswer(question, context);
        try (BedrockRuntimeClient client = BedrockRuntimeClient.builder().region(Region.of(region)).build()) {
            String prompt = "You are an EV business KPI analyst. Use only the aggregate context below; do not invent facts. "
                    + "State assumptions, give practical recommendations and a phased current-to-future roadmap when relevant.\n"
                    + "Context: " + context + "\nQuestion: " + question;
            String body = mapper.writeValueAsString(Map.of(
                    "anthropic_version", "bedrock-2023-05-31",
                    "max_tokens", 700,
                    "messages", new Object[]{Map.of("role", "user", "content", prompt)}));
            String raw = client.invokeModel(InvokeModelRequest.builder().modelId(modelId)
                    .contentType("application/json").accept("application/json")
                    .body(SdkBytes.fromUtf8String(body)).build()).body().asUtf8String();
            JsonNode content = mapper.readTree(raw).path("content");
            if (content.isArray() && !content.isEmpty()) return content.get(0).path("text").asText(raw);
            return raw;
        } catch (Exception ex) {
            return "Bedrock request failed; showing local aggregate context instead. " + localAnswer(question, context);
        }
    }

    private String localAnswer(String question, String context) {
        return "Local KPI assistant (Bedrock is not configured). Question: " + question + ". " + context
                + " Roadmap: (1) govern KPI definitions and data quality; (2) automate customer/product ingestion; "
                + "(3) add validated churn and demand forecasting; (4) operationalize monitored recommendations.";
    }
}
