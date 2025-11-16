package com.example.service2;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class NestedController {
    
    @GetMapping("/nested")
    public String nested() {
        try {
            // Add some processing delay to make traces more visible
            Thread.sleep(100);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        return "Response from nested service";
    }
} 