package com.example.demo;

import java.util.List;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class DemoApplication {

	public static void main(String[] args) {
		SpringApplication.run(DemoApplication.class, args);
	}
	
	@GetMapping("/species")
	public List<String> getSpecies() {
		// Generate timestamp dynamically for each request
        List<String> species = List.of("CHANGED", "SUCCESSFULLY", "TESTING", "DEVTOOLS");
		return species;
	}	  
}

