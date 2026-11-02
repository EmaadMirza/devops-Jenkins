package com.demo;

public class Calculator {
    public int add(int a, int b) { return a + b; }
    public int subtract(int a, int b) { return a - b; }

    public static void main(String[] args) {
        System.out.println("2 + 3 = " + new Calculator().add(2, 3));
    }
}
