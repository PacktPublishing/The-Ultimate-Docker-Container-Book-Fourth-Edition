package com.example.demo;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.reactive.function.client.WebClient;

@RestController
public class HelloController {
    
    @Autowired
    private WebClient webClient;
    
    @GetMapping("/hello")
    public String hello() {
        return "Hello, OpenTelemetry!";
    }
    
    @GetMapping("/test")
    public String test() {
        try {
            // Call service2's /nested endpoint
            String response = webClient.get()
                .uri("http://localhost:8081/nested")
                .retrieve()
                .bodyToMono(String.class)
                .block();
            
            return "Response from /test: " + response;
        } catch (Exception e) {
            return "Error calling service2: " + e.getMessage();
        }
    }
}

@Configuration
class WebClientConfig {
    
    @Bean
    public WebClient webClient() {
        return WebClient.builder()
            .baseUrl("http://localhost:8081")
            .build();
    }
}