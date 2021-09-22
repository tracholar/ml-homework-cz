package com.tracholar.testing;

/**
 * Created by zuoyuan on 2019/7/19.
 */
public class PrivatePartialMockingExample {
    public String methodToTest(){
        return methodToMock("input");
    }
    private String methodToMock(String input) {
        return "REAL VALUE = " + input;
    }
}
