package com.example.library;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class LibraryUnitTests {

	class Calculator {
		int add(int a, int b) {
			return a + b;
		}
	}

	@Test
	void assertCanAddNumbers() {
		// Arrange
		Calculator calculator = new Calculator();
		// Act
		int result = calculator.add(2, 3);
		// Assert
		assert result == 5 : "Expected 5 but got " + result;
	}
}
