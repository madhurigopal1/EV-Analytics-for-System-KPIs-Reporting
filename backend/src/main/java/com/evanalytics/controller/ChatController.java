package com.evanalytics.controller;

import com.evanalytics.dto.ChatRequest;
import com.evanalytics.service.BedrockChatService;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.Map;

@RestController
@RequestMapping("/api/chat")
public class ChatController {
    private final BedrockChatService chat;
    public ChatController(BedrockChatService chat) { this.chat = chat; }
    @PostMapping public Map<String, String> ask(@Valid @RequestBody ChatRequest request) {
        return Map.of("answer", chat.answer(request.question()));
    }
}
