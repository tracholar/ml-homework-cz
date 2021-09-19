package com.tracholar.testing;

/**
 * Created by zuoyuan on 2019/7/19.
 */
public class ClassUnderTest {
    public void methodToTest(){
        final long id = IdGenerator.generateNewId();
        System.out.println(id);
    }
}
