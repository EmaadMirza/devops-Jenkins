package com.demo;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

class CalculatorTest {
    private final Calculator c = new Calculator();

    @Test void testAdd() { assertEquals(6, c.add(2, 3)); }
    @Test void testSubtract() { assertEquals(1, c.subtract(3, 2)); }
}
